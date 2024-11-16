#!/bin/bash
set -e  # Exit on any error

# Setup logging to both console and file
# ${TIMESTAMP} comes from the environment variables passed by webhook
LOG_FILE="/app/logs/ci_${TIMESTAMP}.log"
exec 1> >(tee -a "$LOG_FILE") 2>&1  # Redirect stdout and stderr to both console and file

# Helper function for consistent log formatting
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Helper function for sending notifications
# Could be extended to send emails, Slack messages, etc.
notify() {
    local status=$1    # SUCCESS or FAILURE
    local message=$2   # Detailed message
    log "CI ${status}: ${message}"
    # TODO: Add notification logic (email/slack)
    # Example:
    # curl -X POST -H 'Content-type: application/json' \
    #     --data "{\"text\":\"${status}: ${message}\"}" \
    #     $WEBHOOK_URL
}

# Cleanup function to ensure test environment is removed
# even if tests fail
cleanup() {
    log "Cleaning up test environment..."
    # The '|| true' ensures the script doesn't exit if down fails
    docker-compose -f docker-compose.test.yml down || true
    log "Test environment cleaned up."
    log "Deleting cloned repository..."
    rm -rf repo || true
    log "Repository deleted."
}

# Function to run all tests and health checks
run_tests() {
    log "Running tests..."

    # Start test environment using docker-compose
    log "Starting test environment..."
    docker-compose -f docker-compose.test.yml up -d

    # Give services time to start up
    log "Waiting for services to start..."
    sleep 30
    
    # Run health checks for each service
    local services=("weight" "billing") # I.K. Don't think devops is needed, unlsess we plan tests for devops
    for service in "${services[@]}"; do
        log "Checking health of ${service} service..."
        if ! curl -f "http://${service}:8080/health"; then
            notify "FAILURE" "Health check failed for ${service}"
            cleanup
            return 1  # Return error status
        fi
    done
    # Run application tests
    log "Running application tests..."
    # TODO: Add application tests
    # Example:
    # ./run_tests.sh

    # If tests fail, return error status
    if [ $? -ne 0 ]; then
        notify "FAILURE" "Tests failed"
        cleanup
        return 1
    fi
    
    # If we got here, all tests passed
    notify "SUCCESS" "All tests passed"
    cleanup
    return 0
}

# Function to handle production deployment
deploy_production() {
    # check if docker-compose.prod.yml is up, if yes then down it
    if docker-compose -f docker-compose.prod.yml ps -q | grep -q .; then
        log "Stopping existing production deployment..."
        docker-compose -f docker-compose.prod.yml down
    fi
    log "Deploying to production..."
    # Build and start production environment
    # If the build fails, inform the user and start the production environment without building
    isBuildSuccess=true
    if ! docker-compose -f docker-compose.prod.yml build; then
        isBuildSuccess=false
        log "FAILURE: Build failed. Starting production environment without building..."
    docker-compose -f docker-compose.prod.yml up -d
    if [ "$isBuildSuccess" = false ]; then
        notify "FAILURE" "Production deployment failed"
        exit 1
    fi
    notify "SUCCESS" "Production deployment completed"
}

# Main CI process
main() {
    log "Starting CI process"
    log "Target Branch: ${BRANCH}"
    log "Source Branch: ${SOURCE_BRANCH}"
    log "Commit: ${COMMIT_SHA}"
    
    # Full repository clone
    git clone --depth=1000000 ${REPO_URL} repo
    cd repo
    git fetch --all
    
    if [ "$BRANCH" = "master" ]; then
        if [ ! -z "$SOURCE_BRANCH" ]; then
            # PR merge case
            log "Testing merged PR from ${SOURCE_BRANCH}"
            git checkout ${SOURCE_BRANCH}
            
            if run_tests; then
                log "Tests passed, deploying to production"
                git checkout master
                deploy_production
            else
                notify "FAILURE" "PR tests failed"
                exit 1
            fi
        fi
    else
        # Feature branch push
        log "Testing feature branch ${BRANCH}"
        git checkout ${BRANCH}
        
        if run_tests; then
            notify "SUCCESS" "Feature branch tests passed"
        else
            notify "FAILURE" "Feature branch tests failed"
            exit 1
        fi
    fi
}

# Trap any errors and ensure cleanup happens
trap cleanup EXIT

# Run main function
main                                                                                                                                                                                                            

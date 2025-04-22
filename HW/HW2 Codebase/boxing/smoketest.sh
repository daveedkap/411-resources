#!/bin/bash

# Base URL for the Boxing Flask API. Adjust the host port if needed.
BASE_URL="http://localhost:5001/api"
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health and Database Checks
#
###############################################

check_health() {
  echo "Checking health status..."
  curl -s "$BASE_URL/health" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Health check passed."
  else
    echo "Health check failed."
    exit 1
  fi
}

check_db() {
  echo "Checking database connection..."
  curl -s "$BASE_URL/db-check" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Database check passed."
  else
    echo "Database check failed."
    exit 1
  fi
}

###############################################
#
# Boxer Management Endpoints
#
###############################################

add_boxer() {
  echo "Adding boxer 'Test Boxer'..."
  curl -s -X POST "$BASE_URL/add-boxer" \
    -H "Content-Type: application/json" \
    -d '{"name": "Test Boxer", "weight": 150, "height": 170, "reach": 70.0, "age": 25}' | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer 'Test Boxer' added successfully."
  else
    echo "Failed to add boxer 'Test Boxer'."
    exit 1
  fi
}

add_boxer2() {
  echo "Adding boxer 'Test Boxer 2'..."
  curl -s -X POST "$BASE_URL/add-boxer" \
    -H "Content-Type: application/json" \
    -d '{"name": "Test Boxer 2", "weight": 155, "height": 172, "reach": 71.0, "age": 27}' | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer 'Test Boxer 2' added successfully."
  else
    echo "Failed to add boxer 'Test Boxer 2'."
    exit 1
  fi
}

get_boxer_by_id() {
  echo "Retrieving boxer by ID (1)..."
  curl -s "$BASE_URL/get-boxer-by-id/1" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer retrieved successfully by ID."
  else
    echo "Failed to retrieve boxer by ID."
    exit 1
  fi
}

delete_boxer() {
  echo "Deleting boxer with ID 1..."
  curl -s -X DELETE "$BASE_URL/delete-boxer/1" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer deleted successfully."
  else
    echo "Failed to delete boxer."
    exit 1
  fi
}

###############################################
#
# Ring and Fight Endpoints
#
###############################################

enter_ring() {
  echo "Entering boxer 'Test Boxer' into the ring..."
  curl -s -X POST "$BASE_URL/enter-ring" \
    -H "Content-Type: application/json" \
    -d '{"name": "Test Boxer"}' | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer 'Test Boxer' entered the ring successfully."
  else
    echo "Failed to enter boxer 'Test Boxer' into the ring."
    exit 1
  fi
}

enter_ring2() {
  echo "Entering boxer 'Test Boxer 2' into the ring..."
  curl -s -X POST "$BASE_URL/enter-ring" \
    -H "Content-Type: application/json" \
    -d '{"name": "Test Boxer 2"}' | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxer 'Test Boxer 2' entered the ring successfully."
  else
    echo "Failed to enter boxer 'Test Boxer 2' into the ring."
    exit 1
  fi
}

get_boxers() {
  echo "Retrieving boxers in the ring..."
  curl -s "$BASE_URL/get-boxers" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Boxers retrieved successfully."
  else
    echo "Failed to retrieve boxers."
    exit 1
  fi
}

fight() {
  echo "Initiating fight..."
  curl -s "$BASE_URL/fight" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Fight executed successfully."
  else
    echo "Fight failed."
    exit 1
  fi
}

clear_boxers() {
  echo "Clearing boxers from the ring..."
  curl -s -X POST "$BASE_URL/clear-boxers" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Ring cleared successfully."
  else
    echo "Failed to clear the ring."
    exit 1
  fi
}

get_leaderboard() {
  echo "Retrieving leaderboard..."
  curl -s "$BASE_URL/leaderboard?sort=wins" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Leaderboard retrieved successfully."
  else
    echo "Failed to retrieve leaderboard."
    exit 1
  fi
}

###############################################
#
# Execute Smoketests
#
###############################################

check_health
check_db

# Add and confirm first boxer.
add_boxer
get_boxer_by_id

# Add second boxer.
add_boxer2

# Enter both boxers into the ring.
enter_ring
enter_ring2

# Retrieve boxers in the ring.
get_boxers

# Initiate fight; now that there are two boxers, this should succeed.
fight

# Retrieve leaderboard and clear the ring.
get_leaderboard
clear_boxers

# Optional: Delete boxer (if you wish to test boxer deletion separately)
delete_boxer

echo "All smoketests passed successfully!"

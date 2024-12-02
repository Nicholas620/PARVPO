#!/bin/bash

# Step 1: Build the React app
echo "Building the React app..."
npm run build

# Step 2: Copy the build files to the nginx directory
echo "Copying build files to /var/www/sleep-activity/"
sudo cp -r /root/sleep/front/build/* /var/www/sleep-activity/

# Step 3: Test nginx configuration
echo "Testing nginx configuration..."
sudo nginx -t

# Step 4: Reload nginx to apply changes
echo "Reloading nginx..."
sudo systemctl reload nginx

echo "Deployment completed successfully!"

# Use a lightweight web server image as a parent image
FROM nginx:latest

# Set the working directory in the container
WORKDIR /usr/share/nginx/html

# Copy the frontend files into the container
COPY . /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Command to run the frontend application
CMD ["/usr/share/nginx/html/replacehost.sh"]
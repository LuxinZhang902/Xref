# this is a temporary image for using npm to build the frontend
# it is superseded by the next FROM statement, but we can (and do) copy stuff from it

# production environment -- this FROM statement starts a new image, so only stuff we explicitly copy over from the last one will be kept
FROM nginx:1.21.0-alpine

# Copy the nginx.conf 
COPY nginx.conf /etc/nginx/conf.d/xref.conf
COPY htpasswd /etc/nginx/.htpasswd


# Expose port 80 (Nginx)
EXPOSE 80

# Start the NGINX web server and keep it running in the foreground
CMD [ "nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]

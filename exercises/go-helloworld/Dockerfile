# Create builder image first
FROM golang:alpine AS builder

# Install tools needed for project
# # # NONE

# List project dependencies and install them in same folder. Rebuilt if Gopkg files updated.
WORKDIR /go/src/app
# # # NONE

# Copy entire project and build it. Rebuild when a file changes in project directory.
COPY . .
RUN go mod init && go mod tidy
RUN CGO_ENABLED=0 go build -o helloworld

# Single image target
FROM alpine:latest
EXPOSE 6111
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/app/helloworld ./
CMD ["./helloworld"]

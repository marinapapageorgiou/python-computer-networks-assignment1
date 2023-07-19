import java.net.*;
import java.io.*;

public class Server {
    public static void main(String [] args) throws Exception {
	if (args.length < 1) {
	    System.out.println("usage: Server <port-number>");
	    System.exit(1);
	}
	// the server port passed as a command-line parameter
	int port = Integer.parseInt(args[0]);

	// create a server socket, which is our OS's interface to the
	// network functions of a server application
	ServerSocket server_socket = new ServerSocket(port);

	while(true) {
	    Socket s = server_socket.accept();
	    System.out.println("--- connection from: " + s.getInetAddress());

	    InputStream input = s.getInputStream();
	    int c;
	    while(true) {
		c = input.read();
		if (c == 46 /* '.' */ || c == -1) 
		    break;
		System.out.write(c);
	    }
	    s.close();
	    System.out.println("\n--- connection closed ---");
	}
    }
}

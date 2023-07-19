import java.net.*;
import java.io.*;

public class MultiThreadedServer implements Runnable {
    private ServerSocket server_socket;
    private int active_connections;
    
    public synchronized void output(String address, String message) {
	System.out.println(address + ": " + message);
    }

    public synchronized void open_connection(String address) {
	active_connections += 1;
	System.out.println("--->>>" + address + " (" + active_connections + " active connections)");
    }

    public synchronized void close_connection(String address) {
	active_connections -= 1;
	System.out.println("---<<<" + address + " (" + active_connections + " active connections)");
    }

    public void run() {
	try {
	    while(true) {
		Socket s = server_socket.accept();
		String address = s.getRemoteSocketAddress().toString();

		open_connection(address);

		InputStream input = s.getInputStream();
		BufferedReader reader = new BufferedReader(new InputStreamReader(input));
		String line;
		while((line = reader.readLine()) != null)
		    output(address, line);

		close_connection(address);
		s.close();
	    }
	} catch (Exception ex) {
	    System.err.println(ex);
	    System.err.println("thread terminating.");
	}
    }

    MultiThreadedServer(ServerSocket ss) {
	server_socket = ss;
	active_connections = 0;
    }

    public static void main(String [] args) throws Exception {
	if (args.length < 1) {
	    System.out.println("usage: MultiThreadedServer <port-number> [<thread-count> (default=5)]");
	    System.exit(1);
	}
	// the server port number is the first command-line parameter
	int port = Integer.parseInt(args[0]);

	// optional second parameter is the number of server threads
	// (default = 5)
	int n = 5;
	if (args.length > 1)
	    n = Integer.parseInt(args[1]);
	
	// create a server socket, which is our OS's interface to the
	// network functions of a server application
	ServerSocket server_socket = new ServerSocket(port);

	// create the MultiThreadedServer object that implements the server main loop
	MultiThreadedServer S = new MultiThreadedServer(server_socket);

	// create and start he threads that *run* the main loop
	Thread [] threads = new Thread[n];
	for (int i = 0; i < n; ++i) {
	    threads[i] = new Thread(S);
	    threads[i].start();
	}
	for (int i = 0; i < n; ++i)
	    threads[i].join();

	server_socket.close();
    }
}

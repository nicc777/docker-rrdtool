# Docker for RRDtool

This is a simple docker solution to experiment with the excellent [RRDtool](http://oss.oetiker.ch/rrdtool).

This docker image will start the `rrdcached` daemon and listen on port 5000.

## Building the image and preparing for the first run

	$ docker build -t rrd:latest .

Once built, you can also choose three directories to persist your data.

For example, if you would like to persist in `/tmp`, you can try somethgin like the following:

	$ mkdir /tmp/rrd_data /tmp/rrd_tmp /tmp/rrd_journal

## Start a normal docker instance (daemon mode)

Run the following:

	$ docker run -p 127.0.0.1:5000:5000 -v /tmp/rrd_data:/rrd_data -v \
      /tmp/rrd_tmp:/rrd_tmp -v /tmp/rrd_journal:/rrd_journal \ 
      -d -t rrd:latest

You should see something like this with the `docker ps` command:

	$ docker ps
	CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
	ed5124bca087        rrd:latest          "rrdcached -l 0.0.0.0"   3 seconds ago       Up 2 seconds        127.0.0.1:5000->5000/tcp   jovial_mahavira

## Connecting to the rrdcached service (testing)

To test the service, you can use a normal Telnet client and communicate to the server using the normal RRD text protocol (see [documentation](http://oss.oetiker.ch/rrdtool/doc/rrdcached.en.html)):

	$ telnet 127.0.0.1 5000
    Trying 127.0.0.1...
	Connected to 127.0.0.1.
	Escape character is '^]'.
	CREATE datafile_001.rrd -s 300 -O DS:temp:GAUGE:600:-273:5000 RRA:AVERAGE:0.5:1:1200 RRA:MIN:0.5:12:2400 RRA:MAX:0.5:12:2400 RRA:AVERAGE:0.5:12:2400
	0 RRD created OK
	UPDATE datafile_001.rrd 1483017326:14
	0 errors, enqueued 1 value(s).
	STATS   
	9 Statistics follow
	QueueLength: 0
	UpdatesReceived: 1
	FlushesReceived: 0
	UpdatesWritten: 0
	DataSetsWritten: 0
	TreeNodesNumber: 1
	TreeDepth: 1
	JournalBytes: 98
	JournalRotate: 0
	QUIT
	Connection closed by foreign host.

And there you have it.

## Other stuff

To start the image with an interactive shell:

	$ docker run -p 127.0.0.1:5000:5000 -v /tmp/rrd_data:/rrd_data -v \
      /tmp/rrd_tmp:/rrd_tmp -v /tmp/rrd_journal:/rrd_journal \ 
      -i -t rrd:latest /bin/bash -i

You can then start the `rrdcached` daemon manually with:

	$ rrdcached -l 0.0.0.0:5000 -z 2 -f 3600 -p /rrd_tmp/rrdcached.pid -t 8 -j /rrd_journal -g -b /rrd_data

## Next steps

The `rrdcached` protocol dows not cater for graphing functions, which would have been very nice to have. I will probably create a [Flask](http://flask.pocoo.org/) service for that...
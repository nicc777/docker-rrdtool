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

### Interactive shell

To start the image with an interactive shell:

	$ docker run -p 127.0.0.1:5000:5000 -v /tmp/rrd_data:/rrd_data -v \
      /tmp/rrd_tmp:/rrd_tmp -v /tmp/rrd_journal:/rrd_journal \ 
      -i -t rrd:latest /bin/bash -i

You can then start the `rrdcached` daemon manually with:

	$ rrdcached -l 0.0.0.0:5000 -z 2 -f 3600 -p /rrd_tmp/rrdcached.pid -t 8 -j /rrd_journal -g -b /rrd_data

### Examples

The following examples illustrate how to create an RRD database for 2 random number generators that will store a value every 20 seconds while keeping the data for 1 year. The database is less then 50MiB in size, which is actually impressive taken into account the fast number of data that will be stored.

#### Creating the database

The following is an example CREATE command - first the CLI method:

	$ rrdtool create random_number.rrd --step 30 DS:generator1:GAUGE:60:0:100 DS:generator2:GAUGE:60:0:100 RRA:MIN:0.5:1:1051200 RRA:MAX:0.5:1:1051200 RRA:AVERAGE:0.5:1:1051200

And now the protocol version (enter this into your Telnet session):

	CREATE random_number.rrd -s 30 -O DS:generator1:GAUGE:60:0:100 DS:generator2:GAUGE:60:0:100 RRA:MIN:0.5:1:1051200 RRA:MAX:0.5:1:1051200 RRA:AVERAGE:0.5:1:1051200

<b>Hint</b>: To help you create a RRD database, use a wizard like [this one](http://rrdwizard.appspot.com/rrdcreate.php)...

#### Random number generator

You can use the following bash one liner to add data every 20 seconds in an infinite loop:

	$ while true; do (sleep 1; echo "UPDATE random_number.rrd "`date +%s`":"`echo $((0 + RANDOM % 100))`":"`echo $((0 + RANDOM % 100))`; sleep 1 ; echo QUIT) | telnet 127.0.0.1 5000; sleep 20; done

This take some time, but you can also generate a batch of values quickly using the script in the `examples` directory.

#### Generating a graph

At the moment, the graph cannot be generated through the TCP protocol, but if you enter the interactive console, you can generate a graph with something like the following:

	$ rrdtool graph /rrd_tmp/random_number.png -s 1483041600 -e 1483084800 -S 600 -t 'Random Number Generators Data from 2016-12-29 22:00:00 to 2016-12-30 10:00:00' -w 800 -h 600 -a PNG DEF:g1=/rrd_data/random_number.rrd:generator1:AVERAGE DEF:g2=/rrd_data/random_number.rrd:generator2:AVERAGE  LINE2:g1#000000:Generator_1 AREA:g2#ff000080:Generator_2

The values for `-s` and `-e` is the UNIX timestamp for the start and stop time. You can calculate it easily in Bash with something like the following:

	$ date -d '2016-12-30 10:00:00' +%s
	1483084800

I hope to add a graphing function at some stage using a Flask service (see 'Next Steps' below).

## Next Steps

The `rrdcached` protocol does not cater for graphing functions, which would have been very nice to have. I will probably create a [Flask](http://flask.pocoo.org/) service for that...
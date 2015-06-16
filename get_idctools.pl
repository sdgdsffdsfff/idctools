#!/usr/bin/perl


#download software and put it in the user's home directory
chdir;
my $name="idcenv.tar.gz";
my $url="http://10.16.2.221/$name";
system"curl -o $name $url";
system"tar -zxvf $name 1>/dev/null 2>1&";


#!/usr/bin/perl
use strict;
use 5.010;

download();


say"Coping files";
my $commad="bin/python2.7";
my $newcomm="/usr/bin/python2.7";
my $lib="/usr/lib/python2.7";
my $inc="/usr/include/python2.7";
my $libbak="/usr/lib/python2.7-back";
my $includebak="/usr/include/python2.7-back";
#rename before copy if python2.7 exits
if(-d $libpath){
    rename $lib,"/usr/lib/python2.7-back";
    }
if(-d $incpath){
    rename $inc,"/usr/include/python2.7-back";
}    

if(-f $newcomm){
    rename $newcomm,"/usr/bin/python2.7bak";
}
system"cp $command $newcomm";

system"cp -r include/python2.7  $incpath";
system"cp -r  lib/python2.7  $libpath";

#delet the init files
unlink "include/python2.7";
unlink glob "lib/python2.7/*";
rmdir "lib/python2.7";

system"virtualenv --no-site-packages --python=$newcomm virenv";

chdir "virenv";

#recoerenv
system"cp -r $lib  lib/";
system"cp -r $include  include/";
    
if(-d $libbak){
        unlink glob "/usr/lib/python2.7/*";
        rmdir $lib;
}
rename $libbak;$lib;
if(-d $inc){
    unlink glob "/usr/include/python2.7";
    rmdir $inc;
}
rename $includebak,$inc;


sub download{
    say"Add epal repertory..........";
    system"rpm -ivh http://mirror.nl.leaseweb.net/epel/6/x86_64/epel-release-6-8.noarch.rpm 2>1&";
    say"Install virtual-envirualment";
    exec"yum -y install python-virtualenv";
    say"Install snmp-net...";
    system"yum -y install net-snmp net-snmp-devel net-snmp-utils";
}
#!/usr/bin/perl

# 
# Author: Greg Schueler, ~2005
#
# Released into the public domain.
#

############# begin config ###############

# point at location of Markdown.pm
use lib '/home/username/perl';

# document root for documents.
my $root="/usr/local/my.site.com";

# root for templates
my $tbase="/usr/local/my.site.com/template";

# path of header template
my $header="/head.html";

# path of footer template
my $footer="/foot.html";

############# end config ###############


# trick markdown1.0.1 into thinking we are blosxom.
BEGIN{ $blosxom::version="crap"; }

use CGI qw(:all);
use Markdown;

my $out;

my $title='';
my $head='';
my $group='';
my $foot='';
my $text = param('format') eq 'txt';
print header(-Content_Type=> $text ? "text/plain" : "text/html");

if(path_info() && -f $root.path_info()){

	open(F,"$root".path_info()) || die $!;
	my $file=<F>;
	if($file=~s/<title>(.*?)<\/title>//){
		$title=$1;
		$file.=<F>;
	}
	if($file=~s/<group>(.*?)<\/group>//){
		my $groupf = $1;
		if(-r $root.$groupf){
			open(F2,$root.$groupf)||die $!;
			{local $/;  $group=<F2>; }
			close(F2) || die $!;
		}
		$file.=<F>;
	}
	
	if($file=~s/<template>(.*?)<\/template>//){
		$tbase=$1;
		$file.=<F>;
	}
	{local $/; $file.=<F> }
	close(F) || die $!;
	
	my $hdr = $tbase.$header;

    if(-f $hdr && !$text){
        open(F,$hdr) || die $!;
        {local $/;
        $head.= <F>;
        }
        close(F) || die $!;
    }
	my $ftr = $tbase.$footer;
	if(-f $ftr && ! $text){
        open(F,$ftr) || die $!;
        {local $/;
        $foot= <F>;
        }
        close(F) || die $!;
    }
    
	$head=~s/\$title/$title/se;
	unless($text){
        $out.=$head;
        $out.= &Markdown::Markdown($group.$file);
        my %h;
        $out=~s/(<h(\d))(>(.*?)<\/h\2>)/$_=$4;join("","$1 id=\"",split,"\" $3")/seg;
        #following will unique-ify every <h#> id if you want it.  can't guarantee there's no other id's in the document with the same value though!
        #$out=~s/(<h(\d))(>(.*?)<\/h\2>)/$_=$4;$h=join("",split);my $i; if($h{$h}){$i++ while $h{$i?$h."-$i":$h};}; $h.="-$i" if $i; $h{$h}=1;"$1 id=\"$h\" $3"/seg;
        $out.=$foot;
	}
	if($text){
	   $out.=$file;
	}
	

}else{
	my $txt = &Markdown::Markdown(path_info());
	$out.= $txt;
}



print $out;

exit 0;
1;

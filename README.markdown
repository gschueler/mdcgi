# Markdown CGI

**md.cgi** is a simple CGI script to serve documents (a very basic CMS). It lets you write text files in Markdown format, and have them show up as properly formatted HTML documents on your website.

## links

* [Website](http://github.com/gschueler/mdcgi)
* [Example Site](http://greg.vario.us/software/markdown.html) (original md.cgi site)
* [Quick Markdown Guide](http://github.com/gschueler/mdcgi/blob/master/markdown.txt)
* [Markdown Website](http://daringfireball.net/projects/markdown)

## Configuration of md.cgi

Configuration is at the top of the CGI script. I place it in `/cgi-bin` and use it with [mod_rewrite][1] like in [this .htaccess file][2] . So any request for a file ending in `.text` that resolves to an actual file gets rewritten as a request to the CGI, using the filepath as the `path_info`.

[1]:http://httpd.apache.org/docs/mod/mod_rewrite.html
[2]:http://github.com/gschueler/mdcgi/blob/master/md.htaccess

## How md.cgi works

md.cgi uses the path (known as the "path_info") that is appended to the CGI script URL as a relative path rooted at a point on your filesystem (as defined by your configuration.) It merely runs the file at that path through markdown and surrounds it by header and footer html files before outputting it.

## Other tricks added to md.cgi

When it processes a file, the first lines of the text files it reads get special treatment. It looks for some special lines, in order: `<title>something</title>` and `<group>/some/path</group>`, and `<template>/some/path</template>`.

E.G., as used in the Markdown source for [this page](http://greg.vario.us/software/markdown.html):

    <title>Other Software - by Greg Schueler</title>
    <group>/software/menu.html</group>

If `<title>...` is found, then that line is removed from the file, and the string `$title` in the header.html file gets substituted with the `something` value.

Similarly, if `<group>...` is found, then that line is removed from the file, and whatever file exists at `/some/path` is inserted into the output right after the `header.html` file is printed. The purpose of this is to allow a "menu" file to be included. This page uses that to include links to the other related files seen above. The `<group>` file is also interpreted through Markdown, so it can be written just as easily as the rest of the content if you wish.

`<template>` is used to change the template base dir. By default, base/head.html and base/foot.html are used as the templates.

Also, any `<h1>,<h2>`,... "header" tags get rewritten so that they have an id attribute with a value equal to their content. This is to provide `#anchor` hrefs for the document. `<h2>Chapter 1</h2>` is rewritten as `<h2 id="Chapter1">Chapter 1</h2>`. The `id=` attribute must be a single token to be valid HTML, so the content is stripped of whitespace.

## Version History

* **0.1** Mon Jun 7th, 2010 - initial github import
* (??) initial release 

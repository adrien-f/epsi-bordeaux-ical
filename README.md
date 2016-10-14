# Ical Dumper

Quick Python script for dumping your planning and putting it in Google Calendar and cie. Only works with a specific French IT School.

### Dependencies

You will need Python 3 and pip on your system.

### Getting started

```
pip install git+https://github.com/adrien-f/ical-dumper  # use pip3 if you're running with multiple Python versions
icaldump --website http://ecampusmars.adrienf.space  # Replace the website with your campus one.
```

### How does it work?

You will be prompted for your school planning website root url, your username and password. 

The planning will then be dumped from October 2016 to June 2017 and formatted as an ical file. 

You will then have a `calendar.ics` file in your current working directory.

### License

MIT License

Copyright (c) 2016 Adrien F

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

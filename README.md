# nissan_ecu_hacking

Python code written to utilize the Korlan usb2can hardware to send and receive data over the can-bus on a 2008 Nissan 350z

I highly recommend checking out the `Resources` directory. There's a 2008 Nissan 350z Service and Repair manual in there as well as can bus codes I've discovered (and a link to more)

The long term goal for this project is to have a display (connected to a raspberry pi that connects to OBDII via usb) in my 350z where the upper center console is (I don't have the NAV model).
On this display I want to have metrics and graphs and such, maybe an integration with a gps module and Waze or something similar. 

Once I reach that stage I'll be uploading wiring diagrams and write-ups for my process in case someone wants to replicate it.

Need to download drivers for your Korlan USB2CAN?
* Here is the [official download page](https://www.8devices.com/products/usb2can_korlan)
* Here is the [raspberry pi installation guide](https://www.8devices.com/wiki/korlan:compile-raspberry)
* Here is a [stack overflow post](https://stackoverflow.com/questions/7965437/undefined-reference-to-main-collect2-ld-returned-1-exit-status) that helped me when I faced issues on linux

For the `Resources/helpful_links.txt` file you can either view it manually or add it to your booksmarks via importing/exporting (place them inside your bookmarks.html after you export your current ones, then reimport it).
Inside it is a list of ~40 links that I personally found useful, but YMMV
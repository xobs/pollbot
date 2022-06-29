import datetime
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


def get_commands(debug):
    today = datetime.datetime.today()
    # Turn back time if we're debugging
    if debug:
        today = today - datetime.timedelta(days=7)
    next_monday = today + datetime.timedelta(days=1)
    while next_monday.weekday() != 0:
        next_monday = next_monday + datetime.timedelta(days=1)
    next_monday = datetime.datetime(
        next_monday.year,
        next_monday.month,
        next_monday.day,
        21,
        30,
        0,
        0,
        datetime.timezone(datetime.timedelta(hours=9, minutes=0)),
    )
    close_time = next_monday - datetime.timedelta(days=1)
    # Set the close time to next Monday if we turned back time earlier
    if debug:
        close_time = next_monday + datetime.timedelta(days=7)

    # raid_times = [next_monday]
    days = ["Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    raid_time_str = f"<t:{int(next_monday.timestamp())}:F>"
    current_date = next_monday
    for i in range(6):
        current_date = current_date + datetime.timedelta(days=1)
        raid_time_str += f", <t:{int(current_date.timestamp())}:F>"
        # raid_times.append(current_date)

    print(f"Today: {today}")
    print(f"Next Monday is {next_monday}")
    # print("/quickcreate")
    return f"[template: 25] [title: Blue Mage O12S] [description: What days are you available? = {raid_time_str}] [date: {close_time.day}-{close_time.month}-{close_time.year}] [time: {close_time.hour}:{close_time.minute}] [channel: #scheduling] [advanced: < limit_per_user: 7 > < strawpoll_type: reaction >]"


class MyServer(BaseHTTPRequestHandler):
    COPY_BUTTON_HTML = """<form>
  <div class="input-group">
    <span class="input-group-btn">
      <button class="btn btn-default" type="button" id="copy-button"
          data-toggle="tooltip" data-placement="button"
          title="Copy">
          Copy
      </button>
    </span>
    <input type="text" class="form-control"
        value="{}" placeholder="There was a command here I swear -- Reload the page!" id="copy-input">
  </div>
</form>"""
    COPY_BUTTON_JS = """<script>
    $(document).ready(function() {
  // Initialize the tooltip.
  $('#copy-button').tooltip();

  // When the copy button is clicked, select the value of the text box, attempt
  // to execute the copy command, and trigger event to update tooltip message
  // to indicate whether the text was successfully copied.
  $('#copy-button').bind('click', function() {
    var input = document.querySelector('#copy-input');

    navigator.clipboard.writeText(input.value).then(function() {
      $('#copy-button').trigger('copied', ['Copied!']);
    }, function() {
      /* clipboard write failed */
      input.setSelectionRange(0, input.value.length + 1);
      try {
        var success = document.execCommand('copy');
        if (success) {
            $('#copy-button').trigger('copied', ['Copied!']);
        } else {
            $('#copy-button').trigger('copied', ['Copy with Ctrl-c']);
        }
      } catch (err) {
        $('#copy-button').trigger('copied', ['Copy with Ctrl-c']);
      }
    });

  });

  // Handler for updating the tooltip message.
  $('#copy-button').bind('copied', function(event, message) {
    $(this).attr('title', message)
        .tooltip('fixTitle')
        .tooltip('show')
        .attr('title', "Copy to Clipboard")
        .tooltip('fixTitle');
  });
});
</script>"""

    def print_line(self, s):
        self.wfile.write(bytes(s, "utf-8"))
        self.wfile.write(bytes("\r\n", "utf-8"))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.print_line("<!DOCTYPE html>")
        self.print_line('<html lang="en">')
        self.print_line("<head>")
        self.print_line("<title>Blue Mage Scheduler</title>")
        self.print_line(
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
        )
        self.print_line(
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">'
        )
        self.print_line(
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">'
        )
        self.print_line("</head>")

        self.print_line("<body>")
        self.print_line(
            '<script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>'
        )
        self.print_line(
            '<script src="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>'
        )
        self.print_line(MyServer.COPY_BUTTON_JS)
        self.print_line('<div class="container-fluid">')
        self.print_line("<div>")
        self.print_line("/quickcreate<br>")
        self.print_line("</div>")
        self.print_line("<div>")
        commands = get_commands(False).replace("<", "&lt;")
        self.print_line(MyServer.COPY_BUTTON_HTML.format(commands))
        self.print_line("</div>")
        self.print_line("</div>")
        self.print_line("</body>")
        self.print_line("</html>")


def main():
    hostname = "0.0.0.0"
    port = 5000
    if "PORT" in os.environ:
        port = int(os.environ["PORT"])
    webServer = HTTPServer((hostname, port), MyServer)
    print(f"Server started http://{hostname}:{port}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


if __name__ == "__main__":
    main()

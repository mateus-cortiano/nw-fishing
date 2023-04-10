import time
import cli
import window

from contextlib import suppress
from app import Application
from models import Context

HEADER = """
*** #vadio fishing bot ***

Settings:
- Casting time:            {0.cast_time}
- Equip bait:              {0.equip_bait}
- Equip bait max tries:    {0.equip_bait_max_tries}
- Repair tool:             {0.repair_tool}
- Repair tool every:       {0.repair_tool_every}
- Free cam key:            {0.free_cam_key}
- Move directions:         {0.move_directions}
- Update rate:             {0.update_rate}

(Press ctrl+c to pause)
"""


def mainloop(app: Application, context: Context):
    last_tick = time.time()
    update_delta = context.update_rate / 1000

    while not cli.detect_interrupt():
        if time.time() - last_tick < update_delta:
            time.sleep(1 / 1000)
            continue

        last_tick = time.time()

        cli.print_status(context.runs + 1, app.state.__class__.__qualname__)
        app.next()

    app.clean_up()
    cli.print_paused()

    while True:
        if time.time() - last_tick < update_delta:
            time.sleep(1 / 1000)
            continue

        last_tick = time.time()

        if cli.detect_interrupt():
            raise KeyboardInterrupt

        if cli.detect_resume():
            app.reset()
            break


def main():
    settings = cli.parse_args()
    context = Context(window=window.get_nw_window(), **settings)
    app = Application(context)

    cli.print_header(HEADER.format(context))

    with suppress(KeyboardInterrupt):
        while True:
            mainloop(app, context)

    cli.print_end(context.runs)


if __name__ == "__main__":
    raise SystemExit(main())

from ev_implementations.ev_simulation_base import BaseEV


class EVNoCharge(BaseEV):
    def set_charging_station_as_destination(self):
        # Not used in this implementation
        return

    def run(self):
        while True:
            if not self.deactivated:
                self.generate_random_destination()
                yield self.drive_to_location()
            else:
                yield self.park()

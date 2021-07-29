import datetime
from random import Random

from .Guard import Guard
from django.contrib.auth.models import User
from users.models import UserSettings as UserSettings
from Schedule.models import Settings3 as Settings


class Organizer:

    def __init__(self, days, guards_in_shift, organization, officer, sat_night, users, users_settings):
        self.organized = {}
        self.days = days
        self.guards = []
        self.officer = officer
        self.notes = ""
        self.sat_night = sat_night
        self.guards_in_shift = guards_in_shift
        self.score = 0
        self.users = users
        self.users_settings = users_settings
        self.num_guards = len(users)
        self.note_pad = ["אין מספיק אנשים ביום ", "איו אחמ\"ש ביום ", "מישהו נמצא ביותר מידי ליליות"]

    def initialize_dictionaries(self):
        for i in range(14):
            self.organized["M" + str(i)] = []
            self.organized["A" + str(i)] = []
            self.organized["N" + str(i)] = []

    def reset_organizer(self):
        self.organized = {}
        self.guards = []
        self.officer = ""
        self.notes = ""
        self.sat_night = []

    def build_guards(self):
        index = 0
        users = User.objects.all()
        profiles = UserSettings.objects.all()
        settings = Settings.objects.all().last()
        self.officer = settings.officer
        for user in users:
            user_profile = profiles.filter(user=user).first()
            self.guards[index].name = user_profile.nickname
            self.guards[index].qualityNight = user_profile.night
            self.guards[index].qualitySatNight = user_profile.sat_night
            self.guards[index].qualitySatMorning = user_profile.sat_morning
            if len(user.groups.filter(name="manager")) > 0:
                self.guards[index].authority = True
            index = index + 1

    def day_to_week(self, day):
        if day < 7:
            return 0
        else:
            return 1

    # returns who's available in each morning
    def available_morning(self, day):
        available = []
        if day == 0:
            for guard in self.guards:
                if guard.name in self.days["M" + str(day)] and \
                        guard.name not in self.sat_night and guard.name not in self.organized["M" + str(day)]\
                        and guard.name not in self.organized["A" + str(day)]:
                    if guard.weeks[self.day_to_week(day)].resMorning == -1:
                        available.append(guard)
                    elif guard.weeks[self.day_to_week(day)].resMorning != guard.weeks[self.day_to_week(day)].morning:
                        available.append(guard)
        else:
            for guard in self.guards:
                if guard.name in self.days["M" + str(day)] \
                        and guard.name not in self.organized["N" + str(day - 1)] and \
                        guard.name not in self.organized["M" + str(day)] and \
                        guard.name not in self.organized["A" + str(day)]:
                    if day == 6 or day == 13:
                        if guard.name not in self.organized["N" + str(day)]:
                            available.append(guard)
                    else:
                        if guard.weeks[self.day_to_week(day)].resMorning == -1:
                            available.append(guard)
                        elif guard.weeks[self.day_to_week(day)].resMorning != \
                                guard.weeks[self.day_to_week(day)].morning:
                            available.append(guard)
        return available

    # Chooses guard minimum shifts first if everyone is equal then random without quality
    def choose_guard_regular(self, available, day: int, shift: int):
        num_shifts = []
        r = Random()
        if shift == 0:
            for guard in available:
                num_shifts.append(int(guard.weeks[self.day_to_week(day)].morning))
        else:
            for guard in available:
                num_shifts.append(int(guard.weeks[self.day_to_week(day)].afterNoon))
        if self.array_equal(num_shifts):
            num = r.randrange(len(num_shifts))
        else:
            if not self.multiple_index(num_shifts, min(num_shifts)):
                num = num_shifts.index(min(num_shifts))
            else:
                for item in num_shifts:
                    if item != min(num_shifts):
                        num_index = num_shifts.index(item)
                        num_shifts.remove(item)
                        available.pop(num_index)
                num = r.randrange(len(num_shifts))
        return available[num]

    def multiple_index(self, array, minimum):
        num = 0
        for item in array:
            if item == minimum:
                num = num + 1
        if num > 1:
            return True
        return False

    def array_equal(self, array):
        num = array[0]
        for i in range(len(array)):
            if array[i] != num:
                return False
        return True

    def is_empty(self, array):
        for item in array:
            if item != "":
                return False
        return True

    def is_authority_in_available(self, available):
        for guard in available:
            if guard.authority:
                return True
            if guard.name == self.officer:
                return True
        return False

    def saturday(self, day):
        if day == 5 or day == 6 or day == 12 or day == 13:
            return True
        return False

    # Adds one Guard to morning shift
    def add_to_morning_shift(self, day):
        available = self.available_morning(day)
        if len(self.organized["M" + str(day)]) != 0 or not self.is_authority_in_available(available) or self.saturday(day):
            if not self.is_authority_in_available(available) and len(self.organized["M" + str(day)]) == 0 \
                    and not self.saturday(day):
                self.notes = self.notes + "אין אחמש ביום " + self.number_to_day(day) \
                             + " במשמרת בוקר " + "\n"
            if not self.is_empty(available):
                if not self.saturday(day):
                    guard = self.choose_guard_regular(available, day, 0)
                    guard.weeks[self.day_to_week(day)].morning = guard.weeks[self.day_to_week(day)].morning + 1
                else:
                    guard = self.choose_guard_quality(available, day, 1)
                    guard.qualitySatMorning = int(guard.qualitySatMorning) + 1
                    guard.weeks[self.day_to_week(day)].satMorning = guard.weeks[self.day_to_week(day)].satMorning + 1
                self.organized["M" + str(day)].append(guard.name)
            else:
                if not self.saturday(day):
                    self.notes = self.notes + "אין מספיק אנשים ביום " + \
                                 self.number_to_day(day) + "   במשמרת בוקר" + "\n"
                else:
                    self.notes = self.notes + "אין מספיק אנשים ביום " + \
                                 self.number_to_day(day) + "   במשמרת בוקר סופ\"ש" + "\n"
        else:
            if not self.is_empty(available):
                available_authority = []
                for guard in available:
                    if guard.authority:
                        available_authority.append(guard)
                if self.is_empty(available_authority):
                    for guard in available:
                        if guard.name == self.officer:
                            available_authority.append(guard)
                if self.is_empty(available_authority):
                    self.notes = self.notes + "אין אחמ\"ש ביום " + \
                                 self.number_to_day(day) + "   במשמרת בוקר" + "\n"
                    guard = self.choose_guard_regular(available, day, 0)
                else:
                    guard = self.choose_guard_regular(available_authority, day, 0)
                    if guard.name == self.officer:
                        self.notes = self.notes + self.officer + " הוא האחמ\"ש ביום " + \
                                     self.number_to_day(day) + " במשמרת בוקר" + "\n"
                guard.weeks[self.day_to_week(day)].morning = guard.weeks[self.day_to_week(day)].morning + 1
                self.organized["M" + str(day)].append(guard.name)
            else:
                self.notes = self.notes + "אין מספיק אנשים ביום " + \
                             self.number_to_day(day) + "   במשמרת בוקר" + "\n"

    def available_after_noon(self, day):
        available = []
        for guard in self.guards:
            if guard.name in self.days["A" + str(day)] and not \
                    guard.name in self.organized["A" + str(day)] and not \
                    guard.name in self.organized["M" + str(day)] and not \
                    guard.name in self.organized["N" + str(day)]:
                if guard.weeks[self.day_to_week(day)].resAfterNoon == -1:
                    available.append(guard)
                elif guard.weeks[self.day_to_week(day)].resAfterNoon != guard.weeks[self.day_to_week(day)].afterNoon:
                    available.append(guard)
        return available

    def add_to_after_noon_shift(self, day):
        available = self.available_after_noon(day)
        if not self.is_empty(available):
            guard = self.choose_guard_regular(available, day, 1)
            guard.weeks[self.day_to_week(day)].afterNoon = guard.weeks[self.day_to_week(day)].afterNoon + 1
            self.organized["A" + str(day)].append(guard.name)
        else:
            self.notes = self.notes + "אין מספיק אנשים ביום " + \
                         self.number_to_day(day) + "   במשמרת צהריים" + "\n"

    def available_night(self, day):
        available = []
        for guard in self.guards:
            if guard.name in self.days["N" + str(day)] and not \
                    guard.name in self.organized["N" + str(day)] and not guard.name in self.organized["A" + str(day)]:
                if self.saturday(day):
                    if day == 5 or day == 12:
                        if not guard.name in self.organized["N" + str(day + 1)] and not \
                                guard.name in self.organized["M" + str(day + 1)]:
                            available.append(guard)
                    else:
                        if not guard.name in self.organized["M" + str(day)]:
                            if day == 6:
                                if not guard.name in self.organized["M" + str(day + 1)]:
                                    available.append(guard)
                            else:
                                available.append(guard)
                else:
                    if not guard.name in self.organized["M" + str(day + 1)]:
                        available.append(guard)
        return available

    def array_equal_zero(self, array):
        for item in array:
            if item != 0:
                return False
        return True

    # Chooses guard based on quality and random
    def choose_guard_quality(self, available, day: int, shift: int):
        quality_shifts = []
        r = Random()
        temp_available = []
        for guard in available:
            temp_available.append(guard)
        for guard in available:
            if guard.weeks[0].get_quality(shift) > 0 or guard.weeks[1].get_quality(shift) > 0:
                available.remove(guard)
        if len(available) == 0:
            available = temp_available
        if shift == 0:
            for guard in available:
                quality_shifts.append(int(guard.qualityNight))
        elif shift == 2:
            for guard in available:
                quality_shifts.append(int(guard.qualitySatNight))
        else:
            for guard in available:
                quality_shifts.append(int(guard.qualitySatMorning))
        if self.array_equal_zero(quality_shifts):
            num = r.randrange(len(quality_shifts))
        else:
            if not self.multiple_index(quality_shifts, min(quality_shifts)):
                num = quality_shifts.index(min(quality_shifts))
            else:
                for item in quality_shifts:
                    if item != min(quality_shifts):
                        num_index = quality_shifts.index(item)
                        quality_shifts.remove(item)
                        available.pop(num_index)
                num = r.randrange(len(quality_shifts))
        return available[num]

    # Adds one Guard to night shift
    def add_to_night_shift(self, day, shift: int):
        available = self.available_night(day)
        if not self.is_empty(available):
            guard = self.choose_guard_quality(available, day, shift)
            shift_quality = int(guard.weeks[self.day_to_week(day)].get_quality(shift))
            guard.weeks[self.day_to_week(day)].set_quality(shift, shift_quality + 1)
            shift_quality = int(guard.get_quality(shift))
            guard.set_quality(shift, int(shift_quality + 1))
            self.organized["N" + str(day)].append(guard.name)
        else:
            if not self.saturday(day):
                self.notes = self.notes + "אין מספיק אנשים ביום " + \
                             self.number_to_day(day) + "   במשמרת לילה" + "\n"
            else:
                self.notes = self.notes + "אין מספיק אנשים ביום " + \
                             self.number_to_day(day) + "   במשמרת לילה סופ\"ש" + "\n"

    def number_to_day(self, day):
        st = ""
        if day == 0 or day == 7:
            st = "ראשון"
        elif day == 1 or day == 8:
            st = "שני"
        elif day == 2 or day == 9:
            st = "שלישי"
        elif day == 3 or day == 10:
            st = "רביעי"
        elif day == 4 or day == 11:
            st = "חמישי"
        elif day == 5 or day == 12:
            st = "שישי"
        elif day == 6 or day == 13:
            st = "שבת"
        if day < 7:
            st = st + " בשבוע הראשון "
        else:
            st = st + " בשבוע השני "
        return st

    def remove_from_organized(self, day: int, shift: str, name: str):
        self.organized[shift + str(day)].remove(name)

    def name_to_guard(self, name: str):
        for guard in self.guards:
            if name == guard.name:
                return guard

    def re_organize_weekend(self):
        pass

    def re_organized_night(self):
        too_much_nights = []
        min_guards = self.num_guards_in_nights()
        for guard in self.guards:
            if guard.weeks[0].night + guard.weeks[1].night > min_guards:
                too_much_nights.append(guard)
        if len(too_much_nights) == 0:
            return
        for_index = 0
        while_index = 0
        for guard in too_much_nights:
            for i in range(12):
                if guard.name in self.organized["N" + str(i)]:
                    if len(self.available_night(i)) > 0:
                        self.add_to_night_shift(i, 0)
                        self.remove_from_organized(i, "N", guard.name)
                        guard.qualityNight = guard.qualityNight - 1
                        guard.weeks[self.day_to_week(i)].night = guard.weeks[self.day_to_week(i)].night - 1
                        too_much_nights.remove(guard)
                        break
                    elif (i < 4 or i > 6) and i < 11:
                        available_switch = []
                        for guard_morning in self.organized["M" + str(i + 1)]:
                            if guard_morning in self.days["N" + str(i)]:
                                available_switch.append(self.name_to_guard(guard_morning))
                        if len(available_switch) > 0 and \
                                guard.name in self.organized["M" + str(i + 1)]:
                            switched_guard = self.choose_guard_quality(available_switch, i, 0)
                            self.remove_from_organized(i + 1, "M", switched_guard.name)
                            switched_guard.weeks[self.day_to_week(i + 1)].morning = \
                                switched_guard.weeks[self.day_to_week(i + 1)].morning - 1
                            switched_guard.qualityNight = switched_guard.qualityNight + 1
                            switched_guard.weeks[self.day_to_week(i + 1)].night = \
                                switched_guard.weeks[self.day_to_week(i + 1)].night + 1
                            self.organized["N" + str(i)].append(switched_guard.name)
                            self.remove_from_organized(i, "N", guard.name)
                            guard.qualityNight = guard.qualityNight - 1
                            guard.weeks[self.day_to_week(i)].night = guard.weeks[self.day_to_week(i)].night - 1
                            self.add_to_morning_shift(i + 1)
                            too_much_nights.remove(guard)
                            break

    def night_shift_sum(self):
        sum_shift = 0
        for i in range(12):
            if i != 5 and i != 6:
                sum_shift = sum_shift + self.guards_in_shift["N" + str(i)]
        return sum_shift

    def num_guards_in_nights(self):
        sum_shift = self.night_shift_sum()
        if sum_shift % len(self.guards) == 0:
            return sum_shift / len(self.guards)
        else:
            return sum_shift / len(self.guards) + 1

    def check_empty_shift(self):
        for i in range(14):
            if self.guards_in_shift["M" + str(i)] > 0:
                if len(self.organized["M" + str(i)]) == 0:
                    self.notes = self.notes + "אין אף אחד במשמרת בוקר ביום " + str(i + 1) + "\n"
            if self.guards_in_shift["A" + str(i)] > 0:
                if len(self.organized["A" + str(i)]) == 0:
                    self.notes = self.notes + "אין אף אחד במשמרת צהריים ביום " + str(i + 1) + "\n"
            if self.guards_in_shift["N" + str(i)] > 0:
                if len(self.organized["N" + str(i)]) == 0:
                    self.notes = self.notes + "אין אף אחד במשמרת לילה ביום " + str(i + 1) + "\n"

    def check_min_got(self):
        for guard in self.guards:
            if guard.weeks[0].served > 2 and guard.weeks[0].got < 3:
                self.notes = self.notes + guard.name + "לא קיבל מינימום בשבוע ראשון" + "\n"
            if guard.weeks[1].served > 2 and guard.weeks[1].got < 3:
                self.notes = self.notes + guard.name + "לא קיבל מינימום בשבוע שני" + "\n"

    def get_score(self):
        split_notes = self.notes.split("\n")
        for note in split_notes:
            self.score = self.score + self.score_note(note)

    def score_note(self, line):
        if line.count("  הוא האחמ\"ש ביום  ") > 0:
            return 1
        if line.count("אין מספיק אנשים ביום"):
            return 2
        if line.count("אין אחמש ביום "):
            return 4
        if line.count("חסר במשמרת לילה ביום  "):
            return 11
        if line.count("יש פחות אנשים ביום "):
            return 3
        if line.count("לא קיבל מינימום"):
            return 9
        if line.count("מישהו נמצא ביותר מידי ליליות"):
            return 12
        if line.count("חסר במשמרת בוקר"):
            return 10
        if line.count("חסר מישהו במשמרת לילה סופ\"ש "):
            return 11
        if line.count("חסר מישהו במשמרת בוקר סופ\"ש "):
            return 11
        if line.count("אין אף אחד במשמרת"):
            return 99999
        return 0

    def organize(self):
        users = User.objects.all()
        self.initialize_dictionaries()
        num_guards = len(User.objects.all())
        for i in range(num_guards):
            self.guards.append(Guard())
        self.build_guards()
        startDate = datetime.date(2020, 8, 20)
        dates = []
        for i in range(14):
            dates.append(startDate + datetime.timedelta(i))
        for i in range(self.guards_in_shift["M0"]):
            self.add_to_morning_shift(0)
        for i in range(1, 14):
            for j in range(self.guards_in_shift["M" + str(i)]):
                self.add_to_morning_shift(i)
            if self.saturday(i - 1):
                for j in range(self.guards_in_shift["N" + str(i - 1)]):
                    self.add_to_night_shift(i - 1, 2)
            else:
                for j in range(self.guards_in_shift["N" + str(i - 1)]):
                    self.add_to_night_shift(i - 1, 0)
        for i in range(self.guards_in_shift["N13"]):
            self.add_to_night_shift(13, 2)
        for i in range(14):
            for j in range(self.guards_in_shift["A" + str(i)]):
                self.add_to_after_noon_shift(i)
        self.re_organized_night()
        min_guards = self.num_guards_in_nights()
        for guard in self.guards:
            if guard.weeks[0].night + guard.weeks[1].night > min_guards:
                for i in range(guard.weeks[0].night + guard.weeks[1].night):
                    self.notes = self.notes + "מישהו נמצא ביותר מידי ליליות" + "\n"
            guard.weeks[0].count_served(self.days, guard.name, 0)
            guard.weeks[0].count_got(self.organized, guard.name, 0)
            guard.weeks[1].count_served(self.days, guard.name, 1)
            guard.weeks[1].count_got(self.organized, guard.name, 1)
        self.check_min_got()
        self.check_empty_shift()
        self.get_score()

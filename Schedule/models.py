from time import time
from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
import datetime


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name="תאריך")
    title = models.CharField(max_length=30, verbose_name="כותרת")
    text = models.TextField(blank=True, verbose_name="טקסט")

    def __str__(self):
        return self.title


class Settings3(models.Model):
    submitting = models.BooleanField(default=True, verbose_name="ניתן להגיש/לשנות הגשות")
    pin_code = models.IntegerField(default=1234, verbose_name="קוד זיהוי")
    officer = models.CharField(max_length=20, verbose_name="קצין מתקן")
    city = models.CharField(max_length=100, verbose_name="עיר")
    max_seq0 = models.IntegerField(default=2, verbose_name="מספר רצפים מקסימלי לילה לצהריים")
    max_seq1 = models.IntegerField(default=2, verbose_name="מספר רצפים מקסימלי צהריים לבוקר")

    def __str__(self):
        return "הגדרות"


class Week(models.Model):
    date = models.DateField(default=timezone.now())
    num_week = models.IntegerField(default=0, blank=False)
    Day1_630 = models.TextField(max_length=50, blank=True)
    Day1_700_search = models.TextField(max_length=50, blank=True)
    Day1_700_manager = models.TextField(max_length=50, blank=True)
    Day1_720_1 = models.TextField(max_length=50, blank=True)
    Day1_720_pull = models.TextField(max_length=50, blank=True)
    Day1_720_2 = models.TextField(max_length=50, blank=True)
    Day1_720_3 = models.TextField(max_length=50, blank=True)
    Day1_1400 = models.TextField(max_length=50, blank=True)
    Day1_1500 = models.TextField(max_length=50, blank=True)
    Day1_1500_1900 = models.TextField(max_length=50, blank=True)
    Day1_2300 = models.TextField(max_length=50, blank=True)
    Day1_notes = models.TextField(max_length=50, blank=True)
    Day2_630 = models.TextField(max_length=50, blank=True)
    Day2_700_search = models.TextField(max_length=50, blank=True)
    Day2_700_manager = models.TextField(max_length=50, blank=True)
    Day2_720_1 = models.TextField(max_length=50, blank=True)
    Day2_720_pull = models.TextField(max_length=50, blank=True)
    Day2_720_2 = models.TextField(max_length=50, blank=True)
    Day2_720_3 = models.TextField(max_length=50, blank=True)
    Day2_1400 = models.TextField(max_length=50, blank=True)
    Day2_1500 = models.TextField(max_length=50, blank=True)
    Day2_1500_1900 = models.TextField(max_length=50, blank=True)
    Day2_2300 = models.TextField(max_length=50, blank=True)
    Day2_notes = models.TextField(max_length=50, blank=True)
    Day3_630 = models.TextField(max_length=50, blank=True)
    Day3_700_search = models.TextField(max_length=50, blank=True)
    Day3_700_manager = models.TextField(max_length=50, blank=True)
    Day3_720_1 = models.TextField(max_length=50, blank=True)
    Day3_720_pull = models.TextField(max_length=50, blank=True)
    Day3_720_2 = models.TextField(max_length=50, blank=True)
    Day3_720_3 = models.TextField(max_length=50, blank=True)
    Day3_1400 = models.TextField(max_length=50, blank=True)
    Day3_1500 = models.TextField(max_length=50, blank=True)
    Day3_1500_1900 = models.TextField(max_length=50, blank=True)
    Day3_2300 = models.TextField(max_length=50, blank=True)
    Day3_notes = models.TextField(max_length=50, blank=True)
    Day4_630 = models.TextField(max_length=50, blank=True)
    Day4_700_search = models.TextField(max_length=50, blank=True)
    Day4_700_manager = models.TextField(max_length=50, blank=True)
    Day4_720_1 = models.TextField(max_length=50, blank=True)
    Day4_720_pull = models.TextField(max_length=50, blank=True)
    Day4_720_2 = models.TextField(max_length=50, blank=True)
    Day4_720_3 = models.TextField(max_length=50, blank=True)
    Day4_1400 = models.TextField(max_length=50, blank=True)
    Day4_1500 = models.TextField(max_length=50, blank=True)
    Day4_1500_1900 = models.TextField(max_length=50, blank=True)
    Day4_2300 = models.TextField(max_length=50, blank=True)
    Day4_notes = models.TextField(max_length=50, blank=True)
    Day5_630 = models.TextField(max_length=50, blank=True)
    Day5_700_search = models.TextField(max_length=50, blank=True)
    Day5_700_manager = models.TextField(max_length=50, blank=True)
    Day5_720_1 = models.TextField(max_length=50, blank=True)
    Day5_720_pull = models.TextField(max_length=50, blank=True)
    Day5_720_2 = models.TextField(max_length=50, blank=True)
    Day5_720_3 = models.TextField(max_length=50, blank=True)
    Day5_1400 = models.TextField(max_length=50, blank=True)
    Day5_1500 = models.TextField(max_length=50, blank=True)
    Day5_1500_1900 = models.TextField(max_length=50, blank=True)
    Day5_2300 = models.TextField(max_length=50, blank=True)
    Day5_notes = models.TextField(max_length=50, blank=True)
    Day6_630 = models.TextField(max_length=50, blank=True)
    Day6_700_search = models.TextField(max_length=50, blank=True)
    Day6_700_manager = models.TextField(max_length=50, blank=True)
    Day6_720_1 = models.TextField(max_length=50, blank=True)
    Day6_720_pull = models.TextField(max_length=50, blank=True)
    Day6_720_2 = models.TextField(max_length=50, blank=True)
    Day6_720_3 = models.TextField(max_length=50, blank=True)
    Day6_1400 = models.TextField(max_length=50, blank=True)
    Day6_1500 = models.TextField(max_length=50, blank=True)
    Day6_1500_1900 = models.TextField(max_length=50, blank=True)
    Day6_2300 = models.TextField(max_length=50, blank=True)
    Day6_notes = models.TextField(max_length=50, blank=True)
    Day7_630 = models.TextField(max_length=50, blank=True)
    Day7_700_search = models.TextField(max_length=50, blank=True)
    Day7_700_manager = models.TextField(max_length=50, blank=True)
    Day7_720_1 = models.TextField(max_length=50, blank=True)
    Day7_720_pull = models.TextField(max_length=50, blank=True)
    Day7_720_2 = models.TextField(max_length=50, blank=True)
    Day7_720_3 = models.TextField(max_length=50, blank=True)
    Day7_1400 = models.TextField(max_length=50, blank=True)
    Day7_1500 = models.TextField(max_length=50, blank=True)
    Day7_1500_1900 = models.TextField(max_length=50, blank=True)
    Day7_2300 = models.TextField(max_length=50, blank=True)
    Day7_notes = models.TextField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.date} שבוע {self.num_week + 1}'


class Organization(models.Model):
    date = models.DateField(default=timezone.now)
    num_weeks = models.IntegerField(default=2, blank=False)
    published = models.BooleanField(default=False, verbose_name="פרסום")
    Day1_630 = models.TextField(max_length=50, blank=True)
    Day1_700_search = models.TextField(max_length=50, blank=True)
    Day1_700_manager = models.TextField(max_length=50, blank=True)
    Day1_720_1 = models.TextField(max_length=50, blank=True)
    Day1_720_pull = models.TextField(max_length=50, blank=True)
    Day1_720_2 = models.TextField(max_length=50, blank=True)
    Day1_720_3 = models.TextField(max_length=50, blank=True)
    Day1_1400 = models.TextField(max_length=50, blank=True)
    Day1_1500 = models.TextField(max_length=50, blank=True)
    Day1_1500_1900 = models.TextField(max_length=50, blank=True)
    Day1_2300 = models.TextField(max_length=50, blank=True)
    Day1_notes = models.TextField(max_length=50, blank=True)
    Day2_630 = models.TextField(max_length=50, blank=True)
    Day2_700_search = models.TextField(max_length=50, blank=True)
    Day2_700_manager = models.TextField(max_length=50, blank=True)
    Day2_720_1 = models.TextField(max_length=50, blank=True)
    Day2_720_pull = models.TextField(max_length=50, blank=True)
    Day2_720_2 = models.TextField(max_length=50, blank=True)
    Day2_720_3 = models.TextField(max_length=50, blank=True)
    Day2_1400 = models.TextField(max_length=50, blank=True)
    Day2_1500 = models.TextField(max_length=50, blank=True)
    Day2_1500_1900 = models.TextField(max_length=50, blank=True)
    Day2_2300 = models.TextField(max_length=50, blank=True)
    Day2_notes = models.TextField(max_length=50, blank=True)
    Day3_630 = models.TextField(max_length=50, blank=True)
    Day3_700_search = models.TextField(max_length=50, blank=True)
    Day3_700_manager = models.TextField(max_length=50, blank=True)
    Day3_720_1 = models.TextField(max_length=50, blank=True)
    Day3_720_pull = models.TextField(max_length=50, blank=True)
    Day3_720_2 = models.TextField(max_length=50, blank=True)
    Day3_720_3 = models.TextField(max_length=50, blank=True)
    Day3_1400 = models.TextField(max_length=50, blank=True)
    Day3_1500 = models.TextField(max_length=50, blank=True)
    Day3_1500_1900 = models.TextField(max_length=50, blank=True)
    Day3_2300 = models.TextField(max_length=50, blank=True)
    Day3_notes = models.TextField(max_length=50, blank=True)
    Day4_630 = models.TextField(max_length=50, blank=True)
    Day4_700_search = models.TextField(max_length=50, blank=True)
    Day4_700_manager = models.TextField(max_length=50, blank=True)
    Day4_720_1 = models.TextField(max_length=50, blank=True)
    Day4_720_pull = models.TextField(max_length=50, blank=True)
    Day4_720_2 = models.TextField(max_length=50, blank=True)
    Day4_720_3 = models.TextField(max_length=50, blank=True)
    Day4_1400 = models.TextField(max_length=50, blank=True)
    Day4_1500 = models.TextField(max_length=50, blank=True)
    Day4_1500_1900 = models.TextField(max_length=50, blank=True)
    Day4_2300 = models.TextField(max_length=50, blank=True)
    Day4_notes = models.TextField(max_length=50, blank=True)
    Day5_630 = models.TextField(max_length=50, blank=True)
    Day5_700_search = models.TextField(max_length=50, blank=True)
    Day5_700_manager = models.TextField(max_length=50, blank=True)
    Day5_720_1 = models.TextField(max_length=50, blank=True)
    Day5_720_pull = models.TextField(max_length=50, blank=True)
    Day5_720_2 = models.TextField(max_length=50, blank=True)
    Day5_720_3 = models.TextField(max_length=50, blank=True)
    Day5_1400 = models.TextField(max_length=50, blank=True)
    Day5_1500 = models.TextField(max_length=50, blank=True)
    Day5_1500_1900 = models.TextField(max_length=50, blank=True)
    Day5_2300 = models.TextField(max_length=50, blank=True)
    Day5_notes = models.TextField(max_length=50, blank=True)
    Day6_630 = models.TextField(max_length=50, blank=True)
    Day6_700_search = models.TextField(max_length=50, blank=True)
    Day6_700_manager = models.TextField(max_length=50, blank=True)
    Day6_720_1 = models.TextField(max_length=50, blank=True)
    Day6_720_pull = models.TextField(max_length=50, blank=True)
    Day6_720_2 = models.TextField(max_length=50, blank=True)
    Day6_720_3 = models.TextField(max_length=50, blank=True)
    Day6_1400 = models.TextField(max_length=50, blank=True)
    Day6_1500 = models.TextField(max_length=50, blank=True)
    Day6_1500_1900 = models.TextField(max_length=50, blank=True)
    Day6_2300 = models.TextField(max_length=50, blank=True)
    Day6_notes = models.TextField(max_length=50, blank=True)
    Day7_630 = models.TextField(max_length=50, blank=True)
    Day7_700_search = models.TextField(max_length=50, blank=True)
    Day7_700_manager = models.TextField(max_length=50, blank=True)
    Day7_720_1 = models.TextField(max_length=50, blank=True)
    Day7_720_pull = models.TextField(max_length=50, blank=True)
    Day7_720_2 = models.TextField(max_length=50, blank=True)
    Day7_720_3 = models.TextField(max_length=50, blank=True)
    Day7_1400 = models.TextField(max_length=50, blank=True)
    Day7_1500 = models.TextField(max_length=50, blank=True)
    Day7_1500_1900 = models.TextField(max_length=50, blank=True)
    Day7_2300 = models.TextField(max_length=50, blank=True)
    Day7_notes = models.TextField(max_length=50, blank=True)
    Day8_630 = models.TextField(max_length=50, blank=True)
    Day8_700_search = models.TextField(max_length=50, blank=True)
    Day8_700_manager = models.TextField(max_length=50, blank=True)
    Day8_720_1 = models.TextField(max_length=50, blank=True)
    Day8_720_pull = models.TextField(max_length=50, blank=True)
    Day8_720_2 = models.TextField(max_length=50, blank=True)
    Day8_720_3 = models.TextField(max_length=50, blank=True)
    Day8_1400 = models.TextField(max_length=50, blank=True)
    Day8_1500 = models.TextField(max_length=50, blank=True)
    Day8_1500_1900 = models.TextField(max_length=50, blank=True)
    Day8_2300 = models.TextField(max_length=50, blank=True)
    Day8_notes = models.TextField(max_length=50, blank=True)
    Day9_630 = models.TextField(max_length=50, blank=True)
    Day9_700_search = models.TextField(max_length=50, blank=True)
    Day9_700_manager = models.TextField(max_length=50, blank=True)
    Day9_720_1 = models.TextField(max_length=50, blank=True)
    Day9_720_pull = models.TextField(max_length=50, blank=True)
    Day9_720_2 = models.TextField(max_length=50, blank=True)
    Day9_720_3 = models.TextField(max_length=50, blank=True)
    Day9_1400 = models.TextField(max_length=50, blank=True)
    Day9_1500 = models.TextField(max_length=50, blank=True)
    Day9_1500_1900 = models.TextField(max_length=50, blank=True)
    Day9_2300 = models.TextField(max_length=50, blank=True)
    Day9_notes = models.TextField(max_length=50, blank=True)
    Day10_630 = models.TextField(max_length=50, blank=True)
    Day10_700_search = models.TextField(max_length=50, blank=True)
    Day10_700_manager = models.TextField(max_length=50, blank=True)
    Day10_720_1 = models.TextField(max_length=50, blank=True)
    Day10_720_pull = models.TextField(max_length=50, blank=True)
    Day10_720_2 = models.TextField(max_length=50, blank=True)
    Day10_720_3 = models.TextField(max_length=50, blank=True)
    Day10_1400 = models.TextField(max_length=50, blank=True)
    Day10_1500 = models.TextField(max_length=50, blank=True)
    Day10_1500_1900 = models.TextField(max_length=50, blank=True)
    Day10_2300 = models.TextField(max_length=50, blank=True)
    Day10_notes = models.TextField(max_length=50, blank=True)
    Day11_630 = models.TextField(max_length=50, blank=True)
    Day11_700_search = models.TextField(max_length=50, blank=True)
    Day11_700_manager = models.TextField(max_length=50, blank=True)
    Day11_720_1 = models.TextField(max_length=50, blank=True)
    Day11_720_pull = models.TextField(max_length=50, blank=True)
    Day11_720_2 = models.TextField(max_length=50, blank=True)
    Day11_720_3 = models.TextField(max_length=50, blank=True)
    Day11_1400 = models.TextField(max_length=50, blank=True)
    Day11_1500 = models.TextField(max_length=50, blank=True)
    Day11_1500_1900 = models.TextField(max_length=50, blank=True)
    Day11_2300 = models.TextField(max_length=50, blank=True)
    Day11_notes = models.TextField(max_length=50, blank=True)
    Day12_630 = models.TextField(max_length=50, blank=True)
    Day12_700_search = models.TextField(max_length=50, blank=True)
    Day12_700_manager = models.TextField(max_length=50, blank=True)
    Day12_720_1 = models.TextField(max_length=50, blank=True)
    Day12_720_pull = models.TextField(max_length=50, blank=True)
    Day12_720_2 = models.TextField(max_length=50, blank=True)
    Day12_720_3 = models.TextField(max_length=50, blank=True)
    Day12_1400 = models.TextField(max_length=50, blank=True)
    Day12_1500 = models.TextField(max_length=50, blank=True)
    Day12_1500_1900 = models.TextField(max_length=50, blank=True)
    Day12_2300 = models.TextField(max_length=50, blank=True)
    Day12_notes = models.TextField(max_length=50, blank=True)
    Day13_630 = models.TextField(max_length=50, blank=True)
    Day13_700_search = models.TextField(max_length=50, blank=True)
    Day13_700_manager = models.TextField(max_length=50, blank=True)
    Day13_720_1 = models.TextField(max_length=50, blank=True)
    Day13_720_pull = models.TextField(max_length=50, blank=True)
    Day13_720_2 = models.TextField(max_length=50, blank=True)
    Day13_720_3 = models.TextField(max_length=50, blank=True)
    Day13_1400 = models.TextField(max_length=50, blank=True)
    Day13_1500 = models.TextField(max_length=50, blank=True)
    Day13_1500_1900 = models.TextField(max_length=50, blank=True)
    Day13_2300 = models.TextField(max_length=50, blank=True)
    Day13_notes = models.TextField(max_length=50, blank=True)
    Day14_630 = models.TextField(max_length=50, blank=True)
    Day14_700_search = models.TextField(max_length=50, blank=True)
    Day14_700_manager = models.TextField(max_length=50, blank=True)
    Day14_720_1 = models.TextField(max_length=50, blank=True)
    Day14_720_pull = models.TextField(max_length=50, blank=True)
    Day14_720_2 = models.TextField(max_length=50, blank=True)
    Day14_720_3 = models.TextField(max_length=50, blank=True)
    Day14_1400 = models.TextField(max_length=50, blank=True)
    Day14_1500 = models.TextField(max_length=50, blank=True)
    Day14_1500_1900 = models.TextField(max_length=50, blank=True)
    Day14_2300 = models.TextField(max_length=50, blank=True)
    Day14_notes = models.TextField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.date}'

    def get_absolute_url(self):
        return reverse("organization-update", kwargs={"pk": self.pk})

class Shift1(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    M1 = models.BooleanField(default=False, verbose_name="ראשון בוקר")
    A1 = models.BooleanField(default=False, verbose_name="ראשון צהריים")
    N1 = models.BooleanField(default=False, verbose_name="ראשון לילה")
    P1 = models.BooleanField(default=True, verbose_name="משיכה")
    R1 = models.BooleanField(default=False, verbose_name="תגבור")
    notes1 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M2 = models.BooleanField(default=False, verbose_name="שני בוקר")
    A2 = models.BooleanField(default=False, verbose_name="שני צהריים")
    N2 = models.BooleanField(default=False, verbose_name="שני לילה")
    P2 = models.BooleanField(default=True, verbose_name="משיכה")
    R2 = models.BooleanField(default=False, verbose_name="תגבור")
    notes2 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M3 = models.BooleanField(default=False, verbose_name="שלישי בוקר")
    A3 = models.BooleanField(default=False, verbose_name="שלישי צהריים")
    N3 = models.BooleanField(default=False, verbose_name="שלישי לילה")
    P3 = models.BooleanField(default=True, verbose_name="משיכה")
    R3 = models.BooleanField(default=False, verbose_name="תגבור")
    notes3 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M4 = models.BooleanField(default=False, verbose_name="רביעי בוקר")
    A4 = models.BooleanField(default=False, verbose_name="רביעי צהריים")
    N4 = models.BooleanField(default=False, verbose_name="רביעי לילה")
    P4 = models.BooleanField(default=True, verbose_name="משיכה")
    R4 = models.BooleanField(default=False, verbose_name="תגבור")
    notes4 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M5 = models.BooleanField(default=False, verbose_name="חמישי בוקר")
    A5 = models.BooleanField(default=False, verbose_name="חמישי צהריים")
    N5 = models.BooleanField(default=False, verbose_name="חמישי לילה")
    P5 = models.BooleanField(default=True, verbose_name="משיכה")
    R5 = models.BooleanField(default=False, verbose_name="תגבור")
    notes5 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M6 = models.BooleanField(default=False, verbose_name="שישי בוקר")
    A6 = models.BooleanField(default=False, verbose_name="שישי צהריים")
    N6 = models.BooleanField(default=False, verbose_name="שישי לילה")
    P6 = models.BooleanField(default=True, verbose_name="משיכה")
    R6 = models.BooleanField(default=False, verbose_name="תגבור")
    notes6 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M7 = models.BooleanField(default=False, verbose_name="שבצ בוקר")
    A7 = models.BooleanField(default=False, verbose_name="שבת צהריים")
    N7 = models.BooleanField(default=False, verbose_name="שבת לילה")
    P7 = models.BooleanField(default=True, verbose_name="משיכה")
    R7 = models.BooleanField(default=False, verbose_name="תגבור")
    notes7 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M8 = models.BooleanField(default=False, verbose_name="ראשון בוקר")
    A8 = models.BooleanField(default=False, verbose_name="ראשון צהריים")
    N8 = models.BooleanField(default=False, verbose_name="ראשון לילה")
    P8 = models.BooleanField(default=True, verbose_name="משיכה")
    R8 = models.BooleanField(default=False, verbose_name="תגבור")
    notes8 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M9 = models.BooleanField(default=False, verbose_name="שני בוקר")
    A9 = models.BooleanField(default=False, verbose_name="שני צהריים")
    N9 = models.BooleanField(default=False, verbose_name="שני לילה")
    P9 = models.BooleanField(default=True, verbose_name="משיכה")
    R9 = models.BooleanField(default=False, verbose_name="תגבור")
    notes9 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M10 = models.BooleanField(default=False, verbose_name="שלישי בוקר")
    A10 = models.BooleanField(default=False, verbose_name="שלישי צהריים")
    N10 = models.BooleanField(default=False, verbose_name="שלישי לילה")
    P10 = models.BooleanField(default=True, verbose_name="משיכה")
    R10 = models.BooleanField(default=False, verbose_name="תגבור")
    notes10 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M11 = models.BooleanField(default=False, verbose_name="רביעי בוקר")
    A11 = models.BooleanField(default=False, verbose_name="רביעי צהריים")
    N11 = models.BooleanField(default=False, verbose_name="רביעי לילה")
    P11 = models.BooleanField(default=True, verbose_name="משיכה")
    R11 = models.BooleanField(default=False, verbose_name="תגבור")
    notes11 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M12 = models.BooleanField(default=False, verbose_name="חמישי בוקר")
    A12 = models.BooleanField(default=False, verbose_name="חמישי צהריים")
    N12 = models.BooleanField(default=False, verbose_name="חמישי לילה")
    P12 = models.BooleanField(default=True, verbose_name="משיכה")
    R12 = models.BooleanField(default=False, verbose_name="תגבור")
    notes12 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M13 = models.BooleanField(default=False, verbose_name="שישי בוקר")
    A13 = models.BooleanField(default=False, verbose_name="שישי צהריים")
    N13 = models.BooleanField(default=False, verbose_name="שישי לילה")
    P13 = models.BooleanField(default=True, verbose_name="משיכה")
    R13 = models.BooleanField(default=False, verbose_name="תגבור")
    notes13 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M14 = models.BooleanField(default=False, verbose_name="שבת בוקר")
    A14 = models.BooleanField(default=False, verbose_name="שבת צהרים")
    N14 = models.BooleanField(default=False, verbose_name="שבת לילה")
    P14 = models.BooleanField(default=True, verbose_name="משיכה")
    R14 = models.BooleanField(default=False, verbose_name="תגבור")
    notes14 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    notes = models.TextField(max_length=200, blank=True, verbose_name="הערות")
    seq_night = models.IntegerField(default=0, verbose_name="מ\"ס רצפים לילה לצהריים")
    seq_noon = models.IntegerField(default=0, verbose_name="מ\"ס רצפים צהריים לבוקר")

    def __str__(self):
        return f'{self.username.first_name} {self.username.last_name} ({self.username}) - {self.date}'

    def get_absolute_url(self):
        return reverse("shift-update", kwargs={"pk": self.pk})


class ShiftWeek(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    num_week = models.IntegerField(default=0, blank=False)
    date = models.DateField(default=timezone.now)
    M1 = models.BooleanField(default=False, verbose_name="ראשון בוקר")
    A1 = models.BooleanField(default=False, verbose_name="ראשון צהריים")
    N1 = models.BooleanField(default=False, verbose_name="ראשון לילה")
    P1 = models.BooleanField(default=True, verbose_name="משיכה")
    R1 = models.BooleanField(default=False, verbose_name="תגבור")
    notes1 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M2 = models.BooleanField(default=False, verbose_name="שני בוקר")
    A2 = models.BooleanField(default=False, verbose_name="שני צהריים")
    N2 = models.BooleanField(default=False, verbose_name="שני לילה")
    P2 = models.BooleanField(default=True, verbose_name="משיכה")
    R2 = models.BooleanField(default=False, verbose_name="תגבור")
    notes2 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M3 = models.BooleanField(default=False, verbose_name="שלישי בוקר")
    A3 = models.BooleanField(default=False, verbose_name="שלישי צהריים")
    N3 = models.BooleanField(default=False, verbose_name="שלישי לילה")
    P3 = models.BooleanField(default=True, verbose_name="משיכה")
    R3 = models.BooleanField(default=False, verbose_name="תגבור")
    notes3 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M4 = models.BooleanField(default=False, verbose_name="רביעי בוקר")
    A4 = models.BooleanField(default=False, verbose_name="רביעי צהריים")
    N4 = models.BooleanField(default=False, verbose_name="רביעי לילה")
    P4 = models.BooleanField(default=True, verbose_name="משיכה")
    R4 = models.BooleanField(default=False, verbose_name="תגבור")
    notes4 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M5 = models.BooleanField(default=False, verbose_name="חמישי בוקר")
    A5 = models.BooleanField(default=False, verbose_name="חמישי צהריים")
    N5 = models.BooleanField(default=False, verbose_name="חמישי לילה")
    P5 = models.BooleanField(default=True, verbose_name="משיכה")
    R5 = models.BooleanField(default=False, verbose_name="תגבור")
    notes5 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M6 = models.BooleanField(default=False, verbose_name="שישי בוקר")
    A6 = models.BooleanField(default=False, verbose_name="שישי צהריים")
    N6 = models.BooleanField(default=False, verbose_name="שישי לילה")
    P6 = models.BooleanField(default=True, verbose_name="משיכה")
    R6 = models.BooleanField(default=False, verbose_name="תגבור")
    notes6 = models.CharField(max_length=100, blank=True, verbose_name="הערות")
    M7 = models.BooleanField(default=False, verbose_name="שבצ בוקר")
    A7 = models.BooleanField(default=False, verbose_name="שבת צהריים")
    N7 = models.BooleanField(default=False, verbose_name="שבת לילה")
    P7 = models.BooleanField(default=True, verbose_name="משיכה")
    R7 = models.BooleanField(default=False, verbose_name="תגבור")
    notes7 = models.CharField(max_length=100, blank=True, verbose_name="הערות")

    def __str__(self):
        return f'{self.username.first_name} {self.username.last_name} ({self.username}) - {self.date}'



class Event(models.Model):
    nickname = models.CharField(default="", max_length=20, verbose_name="כינוי", blank=False)
    date2 = models.DateField(default=timezone.now, verbose_name="תאריך")
    description = models.CharField(default="", max_length=50, verbose_name="תאור")
    training = models.BooleanField(default=False, verbose_name="חד יומי")
    night_before = models.BooleanField(default=False, verbose_name="לילה יום לפני")
    morning = models.BooleanField(default=False, verbose_name="בוקר")
    after_noon = models.BooleanField(default=False, verbose_name="צהריים")
    night = models.BooleanField(default=False, verbose_name="לילה")


class IpBan(models.Model):
    ipaddress = models.GenericIPAddressField(verbose_name="כתובת IP")
    num_tries = models.IntegerField(default=0, verbose_name="מספר ניסיונות")


class Gun(models.Model):
    full_name = models.CharField(verbose_name="שם מלא", max_length=50)
    short_name = models.CharField(verbose_name="שם קצר", max_length=20)

    

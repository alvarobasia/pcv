import matplotlib.pyplot as plt


langs = [3206.1048, 3120.8809, 3273.9467, 3174.6808, 3241.9244]
students = range(1, 6)


plt.bar(students, langs, color='green',
        width=0.4)

plt.xlabel("Courses offered")
plt.ylabel("No. of students enrolled")
plt.title("Students enrolled in different courses")
plt.show()

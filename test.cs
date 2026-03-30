using System;
using System.Collections.Generic;
using System.Linq;

// ----- Model -----
class Student
{
    public string Name { get; set; }
    public List<double> Grades { get; set; } = new();

    public Student(string name) => Name = name;

    public double Average => Grades.Count > 0 ? Grades.Average() : 0;

    public string LetterGrade => Average switch
    {
        >= 90 => "A",
        >= 80 => "B",
        >= 70 => "C",
        >= 60 => "D",
        _      => "F"
    };
}

// ----- App -----
var students = new Dictionary<string, Student>(StringComparer.OrdinalIgnoreCase);

while (true)
{
    Console.WriteLine("\n=== Grade Tracker ===");
    Console.WriteLine("1. Add student");
    Console.WriteLine("2. Add grade");
    Console.WriteLine("3. View all students");
    Console.WriteLine("4. View student detail");
    Console.WriteLine("5. Exit");
    Console.Write("Choose: ");

    switch (Console.ReadLine()?.Trim())
    {
        case "1":
            Console.Write("Student name: ");
            var name = Console.ReadLine()?.Trim();
            if (string.IsNullOrEmpty(name)) { Console.WriteLine("Name cannot be empty."); break; }
            if (students.ContainsKey(name)) { Console.WriteLine("Student already exists."); break; }
            students[name] = new Student(name);
            Console.WriteLine($"Added {name}.");
            break;

        case "2":
            Console.Write("Student name: ");
            var sname = Console.ReadLine()?.Trim();
            if (!students.TryGetValue(sname ?? "", out var s)) { Console.WriteLine("Student not found."); break; }
            Console.Write("Grade (0-100): ");
            if (double.TryParse(Console.ReadLine(), out double g) && g >= 0 && g <= 100)
            { s.Grades.Add(g); Console.WriteLine($"Added {g} for {s.Name}."); }
            else Console.WriteLine("Invalid grade.");
            break;

        case "3":
            if (students.Count == 0) { Console.WriteLine("No students yet."); break; }
            Console.WriteLine($"\n{"Name",-20} {"Avg",6} {"Grade",6}");
            Console.WriteLine(new string('-', 36));
            foreach (var st in students.Values.OrderBy(x => x.Name))
                Console.WriteLine($"{st.Name,-20} {st.Average,6:F1} {st.LetterGrade,6}");
            break;

        case "4":
            Console.Write("Student name: ");
            var dname = Console.ReadLine()?.Trim();
            if (!students.TryGetValue(dname ?? "", out var ds)) { Console.WriteLine("Student not found."); break; }
            Console.WriteLine($"\n{ds.Name} — Average: {ds.Average:F1} ({ds.LetterGrade})");
            Console.WriteLine("Grades: " + string.Join(", ", ds.Grades));
            break;

        case "5":
            Console.WriteLine("Goodbye!");
            return;

        default:
            Console.WriteLine("Invalid option.");
            break;
    }
}



/*
Build a C# console application (GradeTracker) using .NET SDK. The app allows users to add students, assign grades, and view averages with letter grades. Implements a Student class with computed properties, a Dictionary<string, Student> for O(1) lookups, LINQ for calculations, and a switch-based menu loop. No external dependencies.
*/
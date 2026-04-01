// Student.cs 

namespace GradeTrackerApp
{
    public class Student
    {
        public string Name { get; set; }
        public List<double> Grades { get; set; } = new List<double>();

        public Student(string name)
        {
            Name = name;
        }

        public double Average
        {
            get
            {
                if (Grades.Count == 0) return 0;
                return Grades.Average();
            }
        }

        public string LetterGrade
        {
            get
            {
                return Average switch
                {
                    >= 90 => "A",
                    >= 80 => "B",
                    >= 70 => "C",
                    >= 60 => "D",
                    _     => "F"
                };
            }
        }

        public override string ToString() => $"{Name} (Avg: {Average:F1} | {LetterGrade})";
    }
}


//Program.cs

namespace GradeTrackerApp
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            ApplicationConfiguration.Initialize();
            Application.Run(new Form1());
        }
    }
}


//Form1.cs
using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace GradeTrackerApp
{
    public partial class Form1 : Form
    {
        // ── Data store ──────────────────────────────────────────
        private List<Student> _students = new List<Student>();

        // ── Controls ────────────────────────────────────────────
        private TextBox txtStudentName;
        private Button  btnAddStudent;
        private ListBox lstStudents;

        private TextBox txtGrade;
        private Button  btnAddGrade;

        private ListView lvwResults;
        private Label    lblSummary;

        private Button btnClear;

        public Form1()
        {
            InitializeComponent();  // Designer-generated setup
            BuildUI();              // Our own UI setup
        }

        // ── Build every control from code ────────────────────────
        private void BuildUI()
        {
            // ── Form itself ──────────────────────────────────────
            this.Text            = "Student Grade Tracker";
            this.Size            = new Size(700, 560);
            this.StartPosition   = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox     = false;
            this.BackColor       = Color.FromArgb(245, 245, 250);
            this.Font            = new Font("Segoe UI", 10f);

            // ── Section: Add Student ─────────────────────────────
            var lblSection1 = new Label
            {
                Text     = "ADD STUDENT",
                Location = new Point(20, 20),
                Size     = new Size(200, 22),
                Font     = new Font("Segoe UI", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(90, 90, 120)
            };

            txtStudentName = new TextBox
            {
                Location    = new Point(20, 48),
                Size        = new Size(220, 30),
                PlaceholderText = "Enter student name..."
            };

            btnAddStudent = new Button
            {
                Text     = "Add Student",
                Location = new Point(250, 46),
                Size     = new Size(120, 32),
                BackColor = Color.FromArgb(79, 70, 229),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Cursor   = Cursors.Hand
            };
            btnAddStudent.FlatAppearance.BorderSize = 0;
            btnAddStudent.Click += BtnAddStudent_Click;

            // ── Section: Student List ────────────────────────────
            var lblSection2 = new Label
            {
                Text     = "STUDENTS",
                Location = new Point(20, 100),
                Size     = new Size(200, 22),
                Font     = new Font("Segoe UI", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(90, 90, 120)
            };

            lstStudents = new ListBox
            {
                Location      = new Point(20, 124),
                Size          = new Size(350, 140),
                BorderStyle   = BorderStyle.FixedSingle,
                BackColor     = Color.White
            };
            lstStudents.SelectedIndexChanged += LstStudents_SelectedIndexChanged;

            // ── Section: Add Grade ───────────────────────────────
            var lblSection3 = new Label
            {
                Text     = "ADD GRADE (select student first)",
                Location = new Point(390, 100),
                Size     = new Size(270, 22),
                Font     = new Font("Segoe UI", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(90, 90, 120)
            };

            txtGrade = new TextBox
            {
                Location        = new Point(390, 124),
                Size            = new Size(120, 30),
                PlaceholderText = "0 – 100"
            };

            btnAddGrade = new Button
            {
                Text      = "Add Grade",
                Location  = new Point(520, 122),
                Size      = new Size(120, 32),
                BackColor = Color.FromArgb(16, 185, 129),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Cursor    = Cursors.Hand
            };
            btnAddGrade.FlatAppearance.BorderSize = 0;
            btnAddGrade.Click += BtnAddGrade_Click;

            // ── Section: Results table ───────────────────────────
            var lblSection4 = new Label
            {
                Text     = "RESULTS",
                Location = new Point(20, 285),
                Size     = new Size(200, 22),
                Font     = new Font("Segoe UI", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(90, 90, 120)
            };

            lvwResults = new ListView
            {
                Location       = new Point(20, 310),
                Size           = new Size(645, 160),
                View           = View.Details,
                FullRowSelect  = true,
                GridLines      = true,
                BorderStyle    = BorderStyle.FixedSingle,
                BackColor      = Color.White
            };
            lvwResults.Columns.Add("Student",      200);
            lvwResults.Columns.Add("Grades",        250);
            lvwResults.Columns.Add("Average",       80);
            lvwResults.Columns.Add("Letter Grade",  100);

            // ── Summary label ────────────────────────────────────
            lblSummary = new Label
            {
                Text      = "",
                Location  = new Point(20, 480),
                Size      = new Size(500, 28),
                ForeColor = Color.FromArgb(79, 70, 229),
                Font      = new Font("Segoe UI", 10f, FontStyle.Bold)
            };

            // ── Clear all button ─────────────────────────────────
            btnClear = new Button
            {
                Text      = "Clear All",
                Location  = new Point(580, 476),
                Size      = new Size(90, 32),
                BackColor = Color.FromArgb(239, 68, 68),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Cursor    = Cursors.Hand
            };
            btnClear.FlatAppearance.BorderSize = 0;
            btnClear.Click += BtnClear_Click;

            // ── Add all controls to the Form ─────────────────────
            this.Controls.AddRange(new Control[]
            {
                lblSection1, txtStudentName, btnAddStudent,
                lblSection2, lstStudents,
                lblSection3, txtGrade, btnAddGrade,
                lblSection4, lvwResults,
                lblSummary,  btnClear
            });
        }

        // ── EVENT: Add Student ────────────────────────────────────
        private void BtnAddStudent_Click(object sender, EventArgs e)
        {
            string name = txtStudentName.Text.Trim();

            if (string.IsNullOrEmpty(name))
            {
                MessageBox.Show("Please enter a student name.",
                    "Validation", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            bool alreadyExists = _students
                .Any(s => s.Name.Equals(name, StringComparison.OrdinalIgnoreCase));

            if (alreadyExists)
            {
                MessageBox.Show($"'{name}' already exists.",
                    "Duplicate", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            _students.Add(new Student(name));
            txtStudentName.Clear();
            RefreshStudentList();
            RefreshResults();
        }

        // ── EVENT: Add Grade ──────────────────────────────────────
        private void BtnAddGrade_Click(object sender, EventArgs e)
        {
            if (lstStudents.SelectedItem == null)
            {
                MessageBox.Show("Please select a student first.",
                    "No Selection", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (!double.TryParse(txtGrade.Text, out double grade)
                || grade < 0 || grade > 100)
            {
                MessageBox.Show("Enter a valid grade between 0 and 100.",
                    "Invalid Grade", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string selectedName = lstStudents.SelectedItem.ToString()!;
            Student? student = _students
                .FirstOrDefault(s => s.Name == selectedName);

            if (student != null)
            {
                student.Grades.Add(grade);
                txtGrade.Clear();
                RefreshResults();
            }
        }

        // ── EVENT: Selection changed ──────────────────────────────
        private void LstStudents_SelectedIndexChanged(object sender, EventArgs e)
        {
            txtGrade.Focus();
        }

        // ── EVENT: Clear all ──────────────────────────────────────
        private void BtnClear_Click(object sender, EventArgs e)
        {
            var result = MessageBox.Show(
                "Are you sure you want to clear all students and grades?",
                "Confirm Clear",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question);

            if (result == DialogResult.Yes)
            {
                _students.Clear();
                RefreshStudentList();
                RefreshResults();
            }
        }

        // ── HELPER: Refresh the ListBox ───────────────────────────
        private void RefreshStudentList()
        {
            lstStudents.Items.Clear();
            foreach (var student in _students)
                lstStudents.Items.Add(student.Name);
        }

        // ── HELPER: Refresh the ListView table ───────────────────
        private void RefreshResults()
        {
            lvwResults.Items.Clear();

            foreach (var student in _students.OrderBy(s => s.Name))
            {
                string gradesText = student.Grades.Count > 0
                    ? string.Join(", ", student.Grades.Select(g => g.ToString("F1")))
                    : "No grades yet";

                var item = new ListViewItem(student.Name);
                item.SubItems.Add(gradesText);
                item.SubItems.Add(student.Average.ToString("F1"));
                item.SubItems.Add(student.LetterGrade);

                // Colour-code the row by letter grade
                item.BackColor = student.LetterGrade switch
                {
                    "A" => Color.FromArgb(220, 252, 231),
                    "B" => Color.FromArgb(219, 234, 254),
                    "C" => Color.FromArgb(254, 249, 195),
                    "D" => Color.FromArgb(255, 237, 213),
                    _   => Color.FromArgb(254, 226, 226)
                };

                lvwResults.Items.Add(item);
            }

            // Class average summary
            if (_students.Count > 0)
            {
                double classAvg = _students
                    .Where(s => s.Grades.Count > 0)
                    .Select(s => s.Average)
                    .DefaultIfEmpty(0)
                    .Average();

                lblSummary.Text =
                    $"Students: {_students.Count}   |   Class Average: {classAvg:F1}";
            }
            else
            {
                lblSummary.Text = "";
            }
        }
    }
}
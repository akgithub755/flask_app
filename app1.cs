@page "/"

@using Microsoft.AspNetCore.Components.Forms;
@using DocumentFormat.OpenXml;
@using DocumentFormat.OpenXml.Packaging;
@using DocumentFormat.OpenXml.Spreadsheet;
@using ExcelReader.Models;
@using System.Collections.ObjectModel;
@using System.Linq;

<PageTitle>Olympic Medals Explorer</PageTitle>

<style>
    .container {
        font-family: 'Segoe UI', sans-serif;
        max-width: 900px;
        margin: 30px auto;
        padding: 0 20px;
    }

    h2 {
        color: #1a1a2e;
        margin-bottom: 20px;
        font-size: 1.6rem;
        border-bottom: 3px solid #e63946;
        padding-bottom: 8px;
    }

    .file-info {
        background: #f0f4ff;
        border-left: 4px solid #457b9d;
        padding: 10px 16px;
        border-radius: 4px;
        margin: 12px 0;
        font-size: 0.9rem;
        color: #333;
    }

    .btn-read {
        background-color: #1d3557;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 0.95rem;
        border-radius: 6px;
        cursor: pointer;
        margin: 12px 0;
        transition: background 0.2s;
    }

    .btn-read:hover {
        background-color: #457b9d;
    }

    .filters {
        display: flex;
        gap: 16px;
        align-items: flex-end;
        flex-wrap: wrap;
        margin: 16px 0 20px 0;
        background: #f8f9fa;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
    }

    .filter-group {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .filter-group label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .filter-group input,
    .filter-group select {
        padding: 8px 12px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        font-size: 0.9rem;
        background: white;
        min-width: 140px;
    }

    .filter-group input:focus,
    .filter-group select:focus {
        outline: none;
        border-color: #457b9d;
        box-shadow: 0 0 0 2px rgba(69, 123, 157, 0.2);
    }

    .btn-clear {
        background: white;
        color: #e63946;
        border: 1px solid #e63946;
        padding: 8px 16px;
        font-size: 0.85rem;
        border-radius: 5px;
        cursor: pointer;
        align-self: flex-end;
        transition: all 0.2s;
    }

    .btn-clear:hover {
        background: #e63946;
        color: white;
    }

    .result-meta {
        font-size: 0.88rem;
        color: #666;
        margin-bottom: 8px;
    }

    .result-meta span {
        font-weight: 600;
        color: #1d3557;
    }

    .table-wrapper {
        height: 350px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }

    thead th {
        position: sticky;
        top: 0;
        background-color: #1d3557;
        color: white;
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    thead th:first-child { border-radius: 8px 0 0 0; }
    thead th:last-child { border-radius: 0 8px 0 0; }

    tbody tr:nth-child(even) {
        background-color: #f8f9fa;
    }

    tbody tr:hover {
        background-color: #e8f0fe;
    }

    tbody td {
        padding: 10px 16px;
        border-bottom: 1px solid #eee;
        color: #333;
    }

    .medal-gold { color: #d4a017; font-weight: 700; }
    .medal-silver { color: #6c757d; font-weight: 700; }
    .medal-bronze { color: #a0522d; font-weight: 700; }

    .badge-gold {
        display: inline-block;
        background: #fff8e1;
        color: #d4a017;
        border: 1px solid #ffe082;
        border-radius: 4px;
        padding: 2px 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .badge-silver {
        display: inline-block;
        background: #f5f5f5;
        color: #6c757d;
        border: 1px solid #bdbdbd;
        border-radius: 4px;
        padding: 2px 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .badge-bronze {
        display: inline-block;
        background: #fbe9e7;
        color: #a0522d;
        border: 1px solid #ffab91;
        border-radius: 4px;
        padding: 2px 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .error-msg {
        color: #e63946;
        background: #fff0f0;
        border: 1px solid #ffc0c0;
        padding: 10px 14px;
        border-radius: 6px;
        margin-top: 10px;
        font-size: 0.9rem;
    }

    .loading {
        color: #457b9d;
        font-style: italic;
        margin-top: 10px;
    }

    .no-results {
        text-align: center;
        padding: 30px;
        color: #888;
        font-style: italic;
    }
</style>

<div class="container">
    <h2>🏅 Olympic Medals Explorer</h2>

    <InputFile OnChange="@SelectFile" accept=".xlsx" />

    @if (file != null)
    {
        if (errorMessage == null)
        {
            <div class="file-info">
                <div><strong>File:</strong> @file.Name</div>
                <div><strong>Size:</strong> @file.Size.ToString("N0") bytes &nbsp;|&nbsp; <strong>Type:</strong> @file.ContentType</div>
            </div>

            <button class="btn-read" type="button" @onclick="ReadFile">
                📂 Read File
            </button>

            @if (!loaded)
            {
                <p class="loading">Loading...</p>
            }
            else
            {
                <!-- Filters -->
                <div class="filters">
                    <div class="filter-group">
                        <label>Year</label>
                        <input type="number"
                               placeholder="e.g. 2004"
                               min="1896"
                               max="2030"
                               @bind="filterYear"
                               @bind:event="oninput" />
                    </div>
                    <div class="filter-group">
                        <label>Medal Type</label>
                        <select @bind="filterMedal">
                            <option value="">— All Medals —</option>
                            <option value="gold">🥇 Gold</option>
                            <option value="silver">🥈 Silver</option>
                            <option value="bronze">🥉 Bronze</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Min Count</label>
                        <input type="number"
                               placeholder="e.g. 5"
                               min="0"
                               @bind="filterMinCount"
                               @bind:event="oninput" />
                    </div>
                    <button class="btn-clear" @onclick="ClearFilters">✕ Clear</button>
                </div>

                <!-- Result summary -->
                <div class="result-meta">
                    Showing <span>@FilteredMedals.Count()</span> of <span>@allMedals.Count</span> rows
                    @if (filterYear.HasValue) { <span> &nbsp;· Year: @filterYear</span> }
                    @if (!string.IsNullOrEmpty(filterMedal)) { <span> &nbsp;· Medal: @filterMedal</span> }
                    @if (filterMinCount.HasValue) { <span> &nbsp;· Min count ≥ @filterMinCount</span> }
                </div>

                <!-- Table -->
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Year</th>
                                <th>Country</th>
                                <th>🥇 Gold</th>
                                <th>🥈 Silver</th>
                                <th>🥉 Bronze</th>
                            </tr>
                        </thead>
                        <tbody>
                            @{
                                var rows = FilteredMedals.ToList();
                            }
                            @if (rows.Count == 0)
                            {
                                <tr><td colspan="5" class="no-results">No results match your filters.</td></tr>
                            }
                            else
                            {
                                foreach (var m in rows)
                                {
                                    <tr>
                                        <td>@m.Year</td>
                                        <td>@m.Country</td>
                                        <td><span class="badge-gold">@m.Gold</span></td>
                                        <td><span class="badge-silver">@m.Silver</span></td>
                                        <td><span class="badge-bronze">@m.Bronze</span></td>
                                    </tr>
                                }
                            }
                        </tbody>
                    </table>
                </div>
            }
        }

        @if (errorMessage != null)
        {
            <p class="error-msg">⚠️ @errorMessage</p>
        }
    }
</div>

@code {
    IBrowserFile? file;
    int MAXFILESIZE = 50000;
    string? errorMessage;
    bool loaded;
    Collection<Medals> allMedals = new();

    // Filter state
    int? filterYear;
    string filterMedal = "";
    int? filterMinCount;

    private IEnumerable<Medals> FilteredMedals
    {
        get
        {
            var q = allMedals.AsEnumerable();

            if (filterYear.HasValue)
                q = q.Where(m => m.Year == filterYear.Value);

            if (!string.IsNullOrEmpty(filterMedal))
            {
                q = filterMedal switch
                {
                    "gold"   => q.Where(m => m.Gold > (filterMinCount ?? 0)),
                    "silver" => q.Where(m => m.Silver > (filterMinCount ?? 0)),
                    "bronze" => q.Where(m => m.Bronze > (filterMinCount ?? 0)),
                    _        => q
                };
            }
            else if (filterMinCount.HasValue)
            {
                // If no specific medal selected but min count set, filter on total
                q = q.Where(m => m.Gold + m.Silver + m.Bronze >= filterMinCount.Value);
            }

            return q;
        }
    }

    private void ClearFilters()
    {
        filterYear = null;
        filterMedal = "";
        filterMinCount = null;
    }

    private void SelectFile(InputFileChangeEventArgs e)
    {
        file = e.File;
        errorMessage = null;
        loaded = false;
        allMedals.Clear();
        ClearFilters();

        if (file.Size >= MAXFILESIZE ||
            file.ContentType != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        {
            errorMessage = "Invalid file: must be .xlsx and under 50KB.";
        }
    }

    private async Task ReadFile()
    {
        try
        {
            var stream = new MemoryStream();
            await file.OpenReadStream(MAXFILESIZE).CopyToAsync(stream);

            SpreadsheetDocument doc = SpreadsheetDocument.Open(stream, false);
            WorkbookPart wbPart = doc.WorkbookPart;
            var sheet = wbPart.Workbook.Descendants<Sheet>()
                            .FirstOrDefault(s => s.Name == "olympic_medals");
            WorksheetPart wsPart = (WorksheetPart)(wbPart.GetPartById(sheet.Id));
            SheetData sheetData = wsPart.Worksheet.Elements<SheetData>().First();

            var stringTable = wbPart.GetPartsOfType<SharedStringTablePart>().FirstOrDefault();
            allMedals.Clear();

            foreach (Row r in sheetData.Elements<Row>())
            {
                if (r.RowIndex! == 1) continue;

                int col = 1;
                var medals = new Medals();
                foreach (Cell c in r.Elements<Cell>())
                {
                    string value = c.InnerText;
                    if (c.DataType?.Value == CellValues.SharedString)
                        value = stringTable.SharedStringTable.ElementAt(int.Parse(value)).InnerText;

                    switch (col)
                    {
                        case 1: medals.Year   = int.Parse(value); break;
                        case 2: medals.Country = value; break;
                        case 3: medals.Gold   = int.Parse(value); break;
                        case 4: medals.Silver = int.Parse(value); break;
                        case 5: medals.Bronze = int.Parse(value); break;
                    }
                    col++;
                }
                allMedals.Add(medals);
            }

            loaded = true;
        }
        catch (Exception)
        {
            errorMessage = "Could not read the Excel file. Please check the file format.";
        }
    }
}

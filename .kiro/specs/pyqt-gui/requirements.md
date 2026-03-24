# Requirements Document

## Introduction

本文档定义了将现有荷载组合计算工具转换为 PyQt 桌面应用程序的需求。新界面将提供直观的图形用户界面，使用户能够方便地选择文件、配置参数、执行计算并查看结果。

## Glossary

- **Main_Window**: 应用程序的主窗口，包含所有功能模块
- **File_Selector**: 文件选择组件，用于选择输入文件
- **Parameter_Panel**: 参数配置面板，用于设置计算参数
- **Result_Viewer**: 结果查看器，用于显示计算结果
- **Progress_Indicator**: 进度指示器，显示计算进度
- **SATWE_File**: SATWE 软件输出的结构内力数据文件
- **Load_Coefficient_File**: 荷载系数 Excel 文件
- **Calculator**: 执行荷载组合计算的核心模块

## Requirements

### Requirement 1: 主窗口布局

**User Story:** 作为用户，我希望有一个清晰的主窗口界面，以便我能够直观地访问所有功能。

#### Acceptance Criteria

1. WHEN the application starts, THE Main_Window SHALL display a window with title "荷载组合计算工具"
2. THE Main_Window SHALL have a minimum size of 800x600 pixels
3. THE Main_Window SHALL contain three main areas: file selection area, parameter configuration area, and result display area
4. WHEN the window is resized, THE Main_Window SHALL adjust the layout proportionally

### Requirement 2: 文件选择功能

**User Story:** 作为用户，我希望能够方便地选择输入文件，以便我能够加载需要计算的数据。

#### Acceptance Criteria

1. THE File_Selector SHALL provide a button to select SATWE output file
2. WHEN the user clicks the SATWE file selection button, THE File_Selector SHALL open a file dialog filtered for text files
3. THE File_Selector SHALL provide a button to select load coefficient Excel file
4. WHEN the user clicks the coefficient file selection button, THE File_Selector SHALL open a file dialog filtered for Excel files (.xlsx)
5. WHEN a file is selected, THE File_Selector SHALL display the file path in a text field
6. WHEN a file larger than 200KB is selected for SATWE file, THE File_Selector SHALL display a warning message
7. THE File_Selector SHALL provide default path for load coefficient file as "data/荷载系数.xlsx"

### Requirement 3: 参数配置功能

**User Story:** 作为用户，我希望能够配置计算参数，以便我能够根据不同项目需求调整计算设置。

#### Acceptance Criteria

1. THE Parameter_Panel SHALL display the current output file path setting
2. THE Parameter_Panel SHALL allow user to modify the output file path
3. WHEN the user clicks the output path selection button, THE Parameter_Panel SHALL open a save file dialog
4. THE Parameter_Panel SHALL provide default output path as "data/荷载组合结果.xlsx"

### Requirement 4: 计算执行功能

**User Story:** 作为用户，我希望能够一键执行计算，以便我能够快速获得荷载组合结果。

#### Acceptance Criteria

1. THE Main_Window SHALL provide a "开始计算" button
2. WHEN the user clicks the calculate button without selecting SATWE file, THE Main_Window SHALL display an error message
3. WHEN the user clicks the calculate button with valid files selected, THE Calculator SHALL execute the load combination calculation
4. WHILE the calculation is in progress, THE Progress_Indicator SHALL display a progress bar or busy indicator
5. WHILE the calculation is in progress, THE Main_Window SHALL disable the calculate button to prevent duplicate execution
6. WHEN the calculation completes successfully, THE Main_Window SHALL display a success message with the output file path
7. IF an error occurs during calculation, THEN THE Main_Window SHALL display an error message with details

### Requirement 5: 结果显示功能

**User Story:** 作为用户，我希望能够在界面中预览计算结果，以便我能够快速验证计算是否正确。

#### Acceptance Criteria

1. WHEN the calculation completes, THE Result_Viewer SHALL display a summary of the results
2. THE Result_Viewer SHALL show the number of columns processed
3. THE Result_Viewer SHALL provide a dropdown to select different columns for preview
4. WHEN a column is selected, THE Result_Viewer SHALL display the first 10 rows of that column's result in a table
5. THE Result_Viewer SHALL provide a button to open the output Excel file directly

### Requirement 6: 日志显示功能

**User Story:** 作为用户，我希望能够查看计算过程的日志，以便我能够了解计算进度和排查问题。

#### Acceptance Criteria

1. THE Main_Window SHALL include a log display area
2. WHEN the application performs any operation, THE Main_Window SHALL append log messages to the log display area
3. THE log display area SHALL be scrollable
4. THE log display area SHALL show timestamps for each log entry
5. THE Main_Window SHALL provide a button to clear the log display

### Requirement 7: 错误处理

**User Story:** 作为用户，我希望应用程序能够优雅地处理错误，以便我能够了解问题并采取相应措施。

#### Acceptance Criteria

1. IF the selected SATWE file cannot be parsed, THEN THE Main_Window SHALL display a descriptive error message
2. IF the load coefficient file cannot be read, THEN THE Main_Window SHALL display a descriptive error message
3. IF the output file cannot be written, THEN THE Main_Window SHALL display a descriptive error message
4. WHEN an error occurs, THE Main_Window SHALL remain responsive and allow the user to retry

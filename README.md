# Life in Weeks Calendar

A beautiful, interactive web application that visualizes your life in weeks. Inspired by the concept that life is finite and precious, this calendar shows each week of your life as a small box, with each row representing a year.

## 🌟 Features

- **Visual Life Calendar**: See your entire life laid out in weeks (52 weeks per year)
- **Real-time Statistics**: Track weeks lived, weeks remaining, age, and life completion percentage
- **Interactive Grid**: 
  - Hover over any week to see details
  - Click to toggle future weeks between "lived" and "future" states
  - Current week is highlighted with a pulsing animation
- **Customizable via YAML**: Load your personal information from a YAML configuration file
- **Life Milestones**: Track and visualize important life events
- **Beautiful Design**: Modern gradient design with smooth animations
- **Responsive**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

1. **Open the website**: Simply open `index.html` in your web browser
2. **View default calendar**: The page loads with example data
3. **Customize your calendar**: Click "Load Configuration" and select your `config.yaml` file

## 📝 Configuration

Create or edit the `config.yaml` file to personalize your calendar:

```yaml
# Personal Information
name: "Your Life"
birthdate: "1981-06-04"  # Format: YYYY-MM-DD
lifeExpectancy: 90  # Expected years of life

# Life Milestones
milestones:
  - age: 0
    title: "Birthday"
  - age: 18
    title: "Graduated High School"
  - age: 22
    title: "Graduated College"
  - age: 25
    title: "Quarter Century"
  - age: 27
    title: "Move to Hong Kong (30 Oct 2008)"
  - age: 29
    title: "Move to Sydney (1 Apr 2011)"
  - age: 32
    title: "Move to New York (13 Aug 2013)"
  - age: 38
    title: "Move to Singapore (2 Sep 2019)"
  - age: 50
    title: "Half Century"
  - age: 65
    title: "Retirement"
  - age: 75
    title: "Seventy-Five"
```

### Configuration Fields

- **name**: Your name or any title for the calendar
- **birthdate**: Your date of birth in YYYY-MM-DD format
- **lifeExpectancy**: Expected lifespan in years (default: 90)
- **milestones**: List of important life events with age and title

## 🎨 Visual Guide

- **Purple/Blue boxes**: Weeks you've already lived
- **Orange box**: Your current week (animated)
- **Gray boxes**: Future weeks yet to come
- **Green checkmarks**: Completed milestones
- **Gray circles**: Future milestones

## 💡 Usage Tips

1. **Reflect on Time**: Each box represents one week - a finite, precious unit of time
2. **Track Progress**: See exactly how much of your life has passed and what remains
3. **Plan Ahead**: Use the milestone feature to set and track life goals
4. **Share**: Customize and share your life calendar with others

## 🛠️ Technical Details

- **Pure HTML/CSS/JavaScript**: No build process required
- **External Dependencies**: 
  - js-yaml library (loaded via CDN) for YAML parsing
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)

## 📂 File Structure

```
.
├── index.html      # Main HTML structure
├── styles.css      # All styling and animations
├── script.js       # Calendar generation and interactivity
├── config.yaml     # Example configuration file
└── README.md       # This file
```

## 🎯 Concept

The "Life in Weeks" calendar is based on the idea popularized by Tim Urban's "Wait But Why" blog. It's a powerful visualization tool that helps you:

- Appreciate the finite nature of life
- Put time in perspective
- Motivate yourself to make the most of each week
- Track your life's journey

## 🔧 Customization

### Modify Default Settings

Edit `script.js` to change the default configuration:

```javascript
let config = {
    name: "Your Life",
    birthdate: "1981-06-04",
    lifeExpectancy: 90,
    milestones: [...]
};
```

### Styling

Edit `styles.css` to customize:
- Colors and gradients
- Box sizes and spacing
- Animations
- Layout and typography

## 📱 Mobile Support

The calendar is fully responsive and works on mobile devices. The grid adjusts for smaller screens while maintaining usability.

## 🤝 Contributing

Feel free to fork, modify, and use this project for your own purposes!

## 📄 License

This project is open source and available for personal and commercial use.

## 🌐 Inspiration

Inspired by:
- Tim Urban's "Your Life in Weeks" from Wait But Why
- Various life calendar visualizations across the web
- The memento mori philosophy of reflecting on mortality

---

**Remember**: Every week counts. Make them meaningful! ⏳

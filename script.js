// Default configuration
let config = {
    name: "Your Life",
    birthdate: "1990-01-01",
    lifeExpectancy: 90,
    milestones: [
        { age: 18, title: "Adulthood" },
        { age: 25, title: "Quarter Century" },
        { age: 30, title: "Thirties" },
        { age: 40, title: "Forties" },
        { age: 50, title: "Half Century" },
        { age: 65, title: "Retirement" },
        { age: 75, title: "Seventy-Five" }
    ]
};

// Calculate age in years
function calculateAge(birthdate) {
    const birth = new Date(birthdate);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    return age;
}

// Calculate weeks lived
function calculateWeeksLived(birthdate) {
    const birth = new Date(birthdate);
    const today = new Date();
    const diffTime = Math.abs(today - birth);
    const diffWeeks = Math.floor(diffTime / (1000 * 60 * 60 * 24 * 7));
    return diffWeeks;
}

// Calculate total weeks in life expectancy
function calculateTotalWeeks(lifeExpectancy) {
    return lifeExpectancy * 52;
}

// Generate calendar
function generateCalendar(birthdate, lifeExpectancy) {
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = '';
    
    const weeksLived = calculateWeeksLived(birthdate);
    const totalWeeks = calculateTotalWeeks(lifeExpectancy);
    const weeksPerYear = 52;
    const years = Math.ceil(totalWeeks / weeksPerYear);
    
    // Set grid to show 52 columns (weeks per year)
    calendar.style.gridTemplateColumns = `repeat(${weeksPerYear}, 12px)`;
    
    for (let week = 0; week < totalWeeks; week++) {
        const weekBox = document.createElement('div');
        weekBox.className = 'week';
        
        if (week < weeksLived) {
            weekBox.classList.add('lived');
        } else if (week === weeksLived) {
            weekBox.classList.add('current');
        } else {
            weekBox.classList.add('future');
        }
        
        // Add hover tooltip
        const year = Math.floor(week / weeksPerYear);
        const weekInYear = (week % weeksPerYear) + 1;
        weekBox.title = `Year ${year}, Week ${weekInYear}`;
        
        // Add click event to toggle state
        weekBox.addEventListener('click', function() {
            if (this.classList.contains('future')) {
                this.classList.remove('future');
                this.classList.add('lived');
            } else if (this.classList.contains('lived') && week >= weeksLived) {
                this.classList.remove('lived');
                this.classList.add('future');
            }
        });
        
        calendar.appendChild(weekBox);
    }
}

// Update statistics
function updateStats(birthdate, lifeExpectancy) {
    const age = calculateAge(birthdate);
    const weeksLived = calculateWeeksLived(birthdate);
    const totalWeeks = calculateTotalWeeks(lifeExpectancy);
    const weeksRemaining = totalWeeks - weeksLived;
    const percentComplete = ((weeksLived / totalWeeks) * 100).toFixed(1);
    
    document.getElementById('age-years').textContent = age;
    document.getElementById('weeks-lived').textContent = weeksLived.toLocaleString();
    document.getElementById('weeks-remaining').textContent = weeksRemaining.toLocaleString();
    document.getElementById('percent-complete').textContent = percentComplete + '%';
}

// Display milestones
function displayMilestones(milestones, birthdate) {
    const container = document.getElementById('milestones');
    container.innerHTML = '<h2>Life Milestones</h2>';
    
    const currentAge = calculateAge(birthdate);
    
    milestones.forEach(milestone => {
        const milestoneDiv = document.createElement('div');
        milestoneDiv.className = 'milestone';
        
        const status = milestone.age <= currentAge ? '✓' : '○';
        const statusColor = milestone.age <= currentAge ? '#10b981' : '#6b7280';
        
        milestoneDiv.innerHTML = `
            <span class="milestone-title" style="color: ${statusColor}">
                ${status} ${milestone.title}
            </span>
            <span class="milestone-age">Age ${milestone.age}</span>
        `;
        
        container.appendChild(milestoneDiv);
    });
}

// Initialize with default config
function initialize() {
    document.getElementById('person-name').textContent = config.name;
    updateStats(config.birthdate, config.lifeExpectancy);
    generateCalendar(config.birthdate, config.lifeExpectancy);
    displayMilestones(config.milestones, config.birthdate);
}

// Load configuration from YAML file
document.getElementById('load-config-btn').addEventListener('click', function() {
    document.getElementById('yaml-input').click();
});

document.getElementById('yaml-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(event) {
        try {
            const yamlContent = event.target.result;
            const loadedConfig = jsyaml.load(yamlContent);
            
            // Update config with loaded values
            config = {
                name: loadedConfig.name || config.name,
                birthdate: loadedConfig.birthdate || config.birthdate,
                lifeExpectancy: loadedConfig.lifeExpectancy || config.lifeExpectancy,
                milestones: loadedConfig.milestones || config.milestones
            };
            
            // Reinitialize with new config
            initialize();
            
            alert('Configuration loaded successfully!');
        } catch (error) {
            alert('Error loading YAML file: ' + error.message);
        }
    };
    reader.readAsText(file);
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', initialize);

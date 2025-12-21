const defaultBirthdate = "1981-06-04";
const BIRTHDAY_TITLE_PATTERN = /^\s*birthday\b/i;

function formatBirthdate(birthdate) {
    const parsedBirthdate = new Date(birthdate);
    if (!isNaN(parsedBirthdate.getTime())) {
        return parsedBirthdate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    }
    return birthdate;
}

function hasYamlParser() {
    return typeof jsyaml !== 'undefined';
}

function isZeroAge(value) {
    return value === 0 || value === '0';
}

// Default configuration
const defaultConfig = {
    name: "Your Life",
    birthdate: defaultBirthdate,
    lifeExpectancy: 90,
    milestones: [
        { age: 18, title: "Graduated High School" },
        { age: 22, title: "Graduated College" },
        { age: 25, title: "Quarter Century" },
        { age: 27, title: "Move to Hong Kong (30 Oct 2008)" },
        { age: 29, title: "Move to Sydney (1 Apr 2011)" },
        { age: 32, title: "Move to New York (13 Aug 2013)" },
        { age: 38, title: "Move to Singapore (2 Sep 2019)" },
        { age: 50, title: "Half Century" },
        { age: 65, title: "Retirement" },
        { age: 75, title: "Seventy-Five" }
    ]
};

function mergeConfig(baseConfig, overrides) {
    const merged = { ...baseConfig, ...(overrides || {}) };
    merged.milestones = ensureBirthdayMilestone(
        overrides?.birthdate || baseConfig.birthdate,
        overrides?.milestones || baseConfig.milestones
    );
    return merged;
}

let config = { ...defaultConfig };

function ensureBirthdayMilestone(birthdate, milestones) {
    const existingMilestones = milestones || [];
    const hasBirthday = existingMilestones.some(
        milestone => isZeroAge(milestone.age) && BIRTHDAY_TITLE_PATTERN.test(milestone.title || '')
    );
    if (hasBirthday) return existingMilestones;
    
    const safeBirthdate = birthdate || defaultConfig.birthdate;
    const formattedBirthdate = formatBirthdate(safeBirthdate);

    return [
        { age: 0, title: `Birthday (${formattedBirthdate})` },
        ...existingMilestones
    ];
}

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

// Initialize with current config
function initialize() {
    document.getElementById('person-name').textContent = config.name;
    updateStats(config.birthdate, config.lifeExpectancy);
    generateCalendar(config.birthdate, config.lifeExpectancy);
    displayMilestones(config.milestones, config.birthdate);
}

// Load default configuration file first (with fallback to inline defaults)
async function loadDefaultConfig() {
    try {
        if (!hasYamlParser()) {
            throw new Error('YAML parser not available.');
        }
        const response = await fetch('config.yaml');
        if (!response.ok) throw new Error(`Default config not found (status ${response.status})`);
        const yamlContent = await response.text();
        const loadedConfig = jsyaml.load(yamlContent, { schema: jsyaml.CORE_SCHEMA }) || {};

        config = mergeConfig(defaultConfig, loadedConfig);
    } catch (error) {
        console.warn('Using inline defaults:', error.message);
        config = mergeConfig(defaultConfig);
    } finally {
        initialize();
    }
}

// Load configuration from YAML file
document.getElementById('load-config-btn').addEventListener('click', function() {
    document.getElementById('yaml-input').click();
});

document.getElementById('yaml-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    if (!hasYamlParser()) {
        alert('YAML parser not available. Please ensure js-yaml is loaded.');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(event) {
        try {
            const yamlContent = event.target.result;
            const loadedConfig = jsyaml.load(yamlContent, { schema: jsyaml.CORE_SCHEMA });
            
            // Update config with loaded values
            config = mergeConfig(config, loadedConfig);
            
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
document.addEventListener('DOMContentLoaded', loadDefaultConfig);

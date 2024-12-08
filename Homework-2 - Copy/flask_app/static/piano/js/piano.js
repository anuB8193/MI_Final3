// Sound mapping object for key codes and sound URLs
const sound = {
    65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// Preload audio files to reduce lag by caching them in an object
const audioCache = {};
Object.keys(sound).forEach(keyCode => {
    const audio = new Audio(sound[keyCode]);
    audioCache[keyCode] = audio;
});

// Select all white and black piano keys
const allKeys = document.querySelectorAll('.white-key, .black-key');

// Show keyboard labels when hovering over keys
allKeys.forEach(key => {
    key.addEventListener('mouseover', () => {
        allKeys.forEach(k => k.classList.add('show-key'));
    });

    key.addEventListener('mouseout', () => {
        allKeys.forEach(k => k.classList.remove('show-key'));
    });
});

// Map keys to their corresponding HTML elements
const keyMapping = {
    'A': document.querySelector('[data-key="A"]'),
    'S': document.querySelector('[data-key="S"]'),
    'D': document.querySelector('[data-key="D"]'),
    'F': document.querySelector('[data-key="F"]'),
    'G': document.querySelector('[data-key="G"]'),
    'H': document.querySelector('[data-key="H"]'),
    'J': document.querySelector('[data-key="J"]'),
    'K': document.querySelector('[data-key="K"]'),
    'L': document.querySelector('[data-key="L"]'),
    ';': document.querySelector('[data-key=";"]'),
    'W': document.querySelector('[data-key="W"]'),
    'E': document.querySelector('[data-key="E"]'),
    'T': document.querySelector('[data-key="T"]'),
    'Y': document.querySelector('[data-key="Y"]'),
    'U': document.querySelector('[data-key="U"]'),
    'O': document.querySelector('[data-key="O"]'),
    'P': document.querySelector('[data-key="P"]')
};

// Initialize an empty string to track the typed sequence
let sequence = "";
const awakenSequence = "weseeyou"; // The secret sequence for awakening

// Event listener for key presses to play sounds and track sequence
document.addEventListener('keydown', (event) => {
    const keyPressed = event.key.toLowerCase();  // Normalize to lowercase for consistency
    const keyElement = keyMapping[keyPressed.toUpperCase()]; // Get the corresponding key element

    // Check if the key matches a piano key and play sound if the sequence isn't complete
    if (keyElement && sound[event.keyCode] && sequence !== awakenSequence) {
        keyElement.classList.add('key-pressed');
        audioCache[event.keyCode].currentTime = 0;
        audioCache[event.keyCode].play();
    }

    // Add the current key to the sequence
    sequence += keyPressed;

    // Use regex to check if the typed sequence matches the secret phrase
    if (new RegExp(awakenSequence + "$").test(sequence)) {
        awakenGreatOldOne();
    }
});

// Event listener for key release to remove the pressed effect
document.addEventListener('keyup', (event) => {
    const keyPressed = event.key.toUpperCase();
    const keyElement = keyMapping[keyPressed];

    if (keyElement) {
        keyElement.classList.remove('key-pressed');
    }
});

// Function to handle the awakening of the Great Old One
const awakenGreatOldOne = () => {
    // Prevent further key presses by removing event listeners
    document.removeEventListener('keydown', null);
    document.removeEventListener('keyup', null);

    // Fade out the piano body
    const pianoBody = document.querySelector('.piano-body');
    pianoBody.style.transition = 'opacity 3s';
    pianoBody.style.opacity = '0';

    // Play creepy sound effect
    const creepySound = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");
    creepySound.play();

    // Replace the piano with the Great Old One image after fade-out
    setTimeout(() => {
        document.querySelector('.piano-container').innerHTML = `
            <div class="great-old-one-wrapper">
                <img src="static/piano/images/texture.jpeg" alt="The Great Old One" class="great-old-one" loading="lazy">
                <h1 class="awoken-text">I have awoken.</h1>
            </div>
        `;
    }, 3000); // 3-second delay to match the fade-out transition
};

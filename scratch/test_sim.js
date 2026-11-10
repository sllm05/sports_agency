
const fs = require('fs');

const html = fs.readFileSync('rea/fm_2d_grid_match.html', 'utf8');

// Simple DOM Mock
const elements = {};
function getOrCreate(id) {
  if (!elements[id]) {
    elements[id] = {
      id,
      innerText: '',
      innerHTML: '',
      value: '',
      className: '',
      style: {},
      children: [],
      appendChild(child) { this.children.push(child); },
      addEventListener() {},
      getContext(type) {
        return {
          clearRect() {},
          save() {},
          restore() {},
          beginPath() {},
          closePath() {},
          arc() {},
          fill() {},
          stroke() {},
          fillRect() {},
          strokeRect() {},
          moveTo() {},
          lineTo() {},
          fillText() {},
          strokeText() {},
          setLineDash() {},
          ellipse() {},
          bezierCurveTo() {},
          quadraticCurveTo() {},
          clip() {},
          createRadialGradient() { return { addColorStop() {} }; },
          createLinearGradient() { return { addColorStop() {} }; },
          measureText() { return { width: 50 }; }
        };
      }
    };
  }
  return elements[id];
}

global.document = {
  getElementById(id) {
    return getOrCreate(id);
  },
  createElement(tag) {
    return {
      tagName: tag,
      innerText: '',
      innerHTML: '',
      value: '',
      className: '',
      style: {},
      appendChild() {},
      addEventListener() {}
    };
  },
  querySelectorAll(sel) {
    return [];
  }
};

global.window = {
  innerWidth: 1200,
  innerHeight: 800,
  onload: null,
  addEventListener() {}
};

let frameCount = 0;
global.requestAnimationFrame = function(cb) {
  frameCount++;
  if (frameCount <= 10) {
    // Run up to 10 frames
    cb(performance.now() + frameCount * 16.6);
  }
};

global.performance = {
  now() { return Date.now(); }
};

// Extract JS
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/i);
if (!scriptMatch) {
  console.error("No script tag found!");
  process.exit(1);
}

try {
  eval(scriptMatch[1]);
  console.log("Script evaluated successfully!");
  
  if (typeof window.onload === 'function') {
    console.log("Calling window.onload (init)...");
    window.onload();
    console.log("window.onload executed successfully!");
    console.log(`Ran ${frameCount} animation frames without errors!`);
    console.log("HUD Action Text:", elements['hudActionText'] ? elements['hudActionText'].innerText : "None");

    // Test timeline functions
    togglePlay();
    console.log("togglePlay to pause executed!");
    togglePlay();
    console.log("togglePlay to play executed!");
    setSpeed(2.0);
    console.log("setSpeed(2.0) executed!");
    onSeekTime(4.2);
    console.log("onSeekTime(4.2) executed!");

    // Test switching player via eval
    eval("onSelectPlayer(3002)");
    console.log("Switched player to 3002!");
    console.log("Card Name:", elements['pCardName'].innerText);
    console.log("Card Club:", elements['pCardClub'].innerText);
  } else {
    console.warn("window.onload is not a function");
  }
} catch (err) {
  console.error("Error during execution:", err);
  process.exit(1);
}

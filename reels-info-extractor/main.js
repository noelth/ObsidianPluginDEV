const { Plugin, Notice } = require('obsidian');

module.exports = class ReelsInfoExtractor extends Plugin {
  onload() {
    console.log('Loading Reels Info Extractor Plugin');

    // Add a command to process the video link
    this.addCommand({
      id: 'process-video-link',
      name: 'Extract Restaurant Info from Video',
      callback: () => this.processVideoLink(),
    });
  }

  onunload() {
    console.log('Unloading Reels Info Extractor Plugin');
  }

  async processVideoLink() {
    const videoLink = await this.promptForLink();
    if (videoLink) {
      new Notice(`Processing video link: ${videoLink}`);
      // Further processing will go here
    }
  }

  async promptForLink() {
    return new Promise((resolve) => {
      const prompt = new Prompt();
      prompt.onSubmit = (value) => resolve(value);
      prompt.open();
    });
  }
};
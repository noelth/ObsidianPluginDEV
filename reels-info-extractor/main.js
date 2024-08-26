const { Plugin, Notice, Modal } = require('obsidian');

module.exports = class ReelsInfoExtractor extends Plugin {
  onload() {
    try {
      console.log('Loading Reels Info Extractor Plugin');

      // Add a command to process the video link
      this.addCommand({
        id: 'process-video-link',
        name: 'Extract Restaurant Info from Video',
        callback: () => this.processVideoLink(),
      });

    } catch (error) {
      console.error('Failed to load Reels Info Extractor Plugin:', error);
      new Notice('Error loading Reels Info Extractor Plugin. Check console for details.');
    }
  }

  onunload() {
    try {
      console.log('Unloading Reels Info Extractor Plugin');
      // Cleanup tasks if any
    } catch (error) {
      console.error('Failed to unload Reels Info Extractor Plugin:', error);
    }
  }

  async processVideoLink() {
    try {
      const videoLink = await this.promptForLink();
      if (videoLink) {
        if (this.validateLink(videoLink)) {
          new Notice(`Processing video link: ${videoLink}`);
          // Further processing will go here
        } else {
          new Notice('Invalid video link. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error processing video link:', error);
      new Notice('Failed to process video link. Check console for details.');
    }
  }

  async promptForLink() {
    // Custom input modal to prompt the user for a video link
    return new Promise((resolve) => {
      const inputModal = new InputModal(this.app, resolve);
      inputModal.open();
    });
  }

  validateLink(link) {
    // Simple validation for YouTube, Instagram, or TikTok links
    const regex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be|instagram\.com|tiktok\.com)\/.+$/;
    return regex.test(link);
  }
}

// Custom modal class for user input
class InputModal extends Modal {
  constructor(app, callback) {
    super(app);
    this.callback = callback;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'Enter Video Link' });

    const inputEl = contentEl.createEl('input', { type: 'text' });
    inputEl.style.width = '100%';

    const submitButton = contentEl.createEl('button', { text: 'Submit' });
    submitButton.style.marginTop = '10px';
    submitButton.addEventListener('click', () => {
      this.callback(inputEl.value);
      this.close();
    });
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}
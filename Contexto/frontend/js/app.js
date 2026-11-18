import { setToken, getToken, isLoggedIn } from './api.js';
import { init as authInit, updateUI as authUpdateUI } from './auth.js';
import { init as leaguesInit } from './leagues.js';
import { init as tournamentsInit, populateSelects } from './tournaments.js';
import { init as predictInit } from './predictions.js';
import { init as lbInit } from './leaderboard.js';

export const App = {
  currentTab: 'auth',

  init() {
    this.setupNavigation();
    authInit();
    if (isLoggedIn()) {
      this.updateAuthUI();
    }
    populateSelects();
    setInterval(populateSelects, 30000);
  },

  setupNavigation() {
    document.querySelectorAll('#nav button').forEach(btn => {
      btn.addEventListener('click', () => {
        this.showTab(btn.dataset.tab);
      });
    });
  },

  showTab(name) {
    this.currentTab = name;
    document.querySelectorAll('#nav button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    const activeBtn = document.querySelector('#nav button[data-tab="' + name + '"]');
    if (activeBtn) activeBtn.classList.add('active');
    const activeTab = document.getElementById('tab-' + name);
    if (activeTab) activeTab.classList.add('active');

    switch (name) {
      case 'auth':
        authInit();
        authUpdateUI();
        break;
      case 'leagues':
        leaguesInit();
        break;
      case 'tournaments':
        tournamentsInit();
        break;
      case 'predict':
        predictInit();
        break;
      case 'leaderboard':
        lbInit();
        break;
    }
  },

  updateAuthUI() {
    authUpdateUI();
  }
};

window.App = App;

App.init();

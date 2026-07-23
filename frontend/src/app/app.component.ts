/**
 * TaskFlow Frontend - Root Component
 */

import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <header class="header">
      <div class="container">
        <h1 class="logo">
          <a routerLink="/">📋 TaskFlow</a>
        </h1>
        <nav>
          <a routerLink="/tasks" class="nav-link">Tasks</a>
          <a routerLink="/tasks/new" class="nav-link btn-primary">+ New Task</a>
        </nav>
      </div>
    </header>
    
    <main class="container">
      <router-outlet></router-outlet>
    </main>
    
    <footer class="footer">
      <div class="container">
        <p>TaskFlow - Context Orchestrator POC</p>
      </div>
    </footer>
  `,
  styles: [`
    .header {
      background: #1a1a2e;
      color: white;
      padding: 1rem 0;
      margin-bottom: 2rem;
    }
    
    .header .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .logo a {
      color: white;
      text-decoration: none;
      font-size: 1.5rem;
    }
    
    .nav-link {
      color: white;
      text-decoration: none;
      margin-left: 1.5rem;
      padding: 0.5rem 1rem;
      border-radius: 4px;
    }
    
    .nav-link:hover {
      background: rgba(255,255,255,0.1);
    }
    
    .btn-primary {
      background: #4361ee;
    }
    
    .btn-primary:hover {
      background: #3a56d4;
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1rem;
    }
    
    .footer {
      margin-top: 3rem;
      padding: 1rem 0;
      text-align: center;
      color: #666;
      border-top: 1px solid #eee;
    }
  `]
})
export class AppComponent {
  title = 'TaskFlow';
}

import { Outlet } from "react-router-dom";

import AppNavigation from "../components/AppNavigation";
import "./AppLayout.css";

function AppLayout() {
  return (
    <div className="app-layout">
      <header className="app-header">
        <div>
          <span className="app-header__logo">Evolv</span>
          <span className="app-header__subtitle">
            Sua evolução, todos os dias.
          </span>
        </div>
      </header>

      <AppNavigation />

      <main className="app-content">
        <Outlet />
      </main>
    </div>
  );
}

export default AppLayout;
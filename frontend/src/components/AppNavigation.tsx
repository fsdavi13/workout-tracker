import {
  Dumbbell,
  House,
  PersonStanding,
  Utensils,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import "./AppNavigation.css";

const navigationItems = [
  {
    label: "Início",
    path: "/",
    icon: House,
  },
  {
    label: "Academia",
    path: "/academia",
    icon: Dumbbell,
  },
  {
    label: "Corridas",
    path: "/corridas",
    icon: PersonStanding,
  },
  {
    label: "Dieta",
    path: "/dieta",
    icon: Utensils,
  },
];

function AppNavigation() {
  return (
    <nav
      className="app-navigation"
      aria-label="Navegação principal"
    >
      {navigationItems.map((item) => {
        const Icon = item.icon;

        return (
          <NavLink
            key={item.path}
            className={({ isActive }) =>
              [
                "app-navigation__link",
                isActive
                  ? "app-navigation__link--active"
                  : "",
              ]
                .filter(Boolean)
                .join(" ")
            }
            end={item.path === "/"}
            to={item.path}
          >
            <Icon
              aria-hidden="true"
              className="app-navigation__icon"
              size={22}
              strokeWidth={2}
            />

            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}

export default AppNavigation;
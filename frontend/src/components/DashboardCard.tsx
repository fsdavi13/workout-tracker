import type { LucideIcon } from "lucide-react";

import "./DashboardCard.css";

interface DashboardCardProps {
  titulo: string;
  valor: string | number;
  descricao: string;
  icone: LucideIcon;
}

function DashboardCard({
  titulo,
  valor,
  descricao,
  icone: Icone,
}: DashboardCardProps) {
  return (
    <article className="dashboard-card">
      <div className="dashboard-card__header">
        <span className="dashboard-card__title">
          {titulo}
        </span>

        <Icone
          aria-hidden="true"
          className="dashboard-card__icon"
          size={20}
        />
      </div>

      <strong className="dashboard-card__value">
        {valor}
      </strong>

      <span className="dashboard-card__description">
        {descricao}
      </span>
    </article>
  );
}

export default DashboardCard;
import { Link } from "react-router-dom";

function NotFoundPage() {
  return (
    <section className="page page--centered">
      <h1>Página não encontrada</h1>

      <Link className="button" to="/">
        Voltar ao Dashboard
      </Link>
    </section>
  );
}

export default NotFoundPage;
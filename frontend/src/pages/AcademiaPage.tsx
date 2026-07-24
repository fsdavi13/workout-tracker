import axios from "axios";
import {
  Dumbbell,
  Plus,
  Search,
  X,
} from "lucide-react";
import {
  type ChangeEvent,
  type FormEvent,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  criarExercicio,
  listarExercicios,
} from "../services/academiaService";
import type {
  Exercicio,
  ExercicioPayload,
} from "../types/academia";

import "./AcademiaPage.css";

const formularioInicial: ExercicioPayload = {
  nome: "",
  grupo_muscular: "",
};

function normalizarTexto(texto: string): string {
  return texto
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .trim();
}

function obterMensagemErro(erro: unknown): string {
  if (axios.isAxiosError(erro)) {
    const detalhe = erro.response?.data?.detail;

    if (typeof detalhe === "string") {
      return detalhe;
    }
  }

  return "Não foi possível concluir a operação.";
}

function AcademiaPage() {
  const [exercicios, setExercicios] = useState<
    Exercicio[]
  >([]);

  const [pesquisa, setPesquisa] = useState("");
  const [formulario, setFormulario] =
    useState<ExercicioPayload>(formularioInicial);

  const [modalAberto, setModalAberto] = useState(false);
  const [carregando, setCarregando] = useState(true);
  const [salvando, setSalvando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [erroFormulario, setErroFormulario] =
    useState<string | null>(null);

  useEffect(() => {
    async function carregarExercicios() {
      try {
        setCarregando(true);
        setErro(null);

        const dados = await listarExercicios();
        setExercicios(dados);
      } catch {
        setErro(
          "Não foi possível carregar os exercícios.",
        );
      } finally {
        setCarregando(false);
      }
    }

    void carregarExercicios();
  }, []);

  const exerciciosFiltrados = useMemo(() => {
    const termo = normalizarTexto(pesquisa);

    if (!termo) {
      return exercicios;
    }

    return exercicios.filter((exercicio) => {
      const nome = normalizarTexto(exercicio.nome);
      const grupo = normalizarTexto(
        exercicio.grupo_muscular,
      );

      return nome.includes(termo) || grupo.includes(termo);
    });
  }, [exercicios, pesquisa]);

  const sugestoes = useMemo(() => {
    const termo = normalizarTexto(formulario.nome);

    if (!termo) {
      return [];
    }

    return exercicios
      .filter((exercicio) =>
        normalizarTexto(exercicio.nome).includes(termo),
      )
      .slice(0, 5);
  }, [exercicios, formulario.nome]);

  function abrirModal() {
    setFormulario(formularioInicial);
    setErroFormulario(null);
    setModalAberto(true);
  }

  function fecharModal() {
    if (salvando) {
      return;
    }

    setModalAberto(false);
    setFormulario(formularioInicial);
    setErroFormulario(null);
  }

  function atualizarCampo(
    evento: ChangeEvent<
      HTMLInputElement | HTMLSelectElement
    >,
  ) {
    const { name, value } = evento.target;

    setFormulario((dadosAtuais) => ({
      ...dadosAtuais,
      [name]: value,
    }));

    setErroFormulario(null);
  }

  function selecionarSugestao(exercicio: Exercicio) {
    setFormulario({
      nome: exercicio.nome,
      grupo_muscular: exercicio.grupo_muscular,
    });
  }

  async function enviarFormulario(
    evento: FormEvent<HTMLFormElement>,
  ) {
    evento.preventDefault();

    const nome = formulario.nome.trim();
    const grupoMuscular =
      formulario.grupo_muscular.trim();

    if (!nome || !grupoMuscular) {
      setErroFormulario(
        "Preencha o nome e o grupo muscular.",
      );
      return;
    }

    try {
      setSalvando(true);
      setErroFormulario(null);

      const exercicioCriado = await criarExercicio({
        nome,
        grupo_muscular: grupoMuscular,
      });

      setExercicios((exerciciosAtuais) =>
        [...exerciciosAtuais, exercicioCriado].sort(
          (primeiro, segundo) =>
            primeiro.nome.localeCompare(
              segundo.nome,
              "pt-BR",
            ),
        ),
      );

      fecharModal();
    } catch (erroCriacao) {
      setErroFormulario(
        obterMensagemErro(erroCriacao),
      );
    } finally {
      setSalvando(false);
    }
  }

  return (
    <section className="page">
      <header className="page__header academia-header">
        <div>
          <p className="page__eyebrow">Treinamento</p>
          <h1>Academia</h1>
          <p>
            Cadastre seus exercícios e acompanhe seus
            treinos.
          </p>
        </div>

        <button
          className="academia-new-button"
          type="button"
          onClick={abrirModal}
        >
          <Plus size={18} aria-hidden="true" />
          Novo exercício
        </button>
      </header>

      <div className="academia-toolbar">
        <Search
          className="academia-search__icon"
          size={19}
          aria-hidden="true"
        />

        <input
          type="search"
          value={pesquisa}
          onChange={(evento) =>
            setPesquisa(evento.target.value)
          }
          placeholder="Pesquisar por exercício ou grupo muscular"
          aria-label="Pesquisar exercícios"
        />
      </div>

      {carregando && (
        <p className="academia-status">
          Carregando exercícios...
        </p>
      )}

      {!carregando && erro && (
        <div className="academia-message academia-message--error">
          {erro}
        </div>
      )}

      {!carregando &&
        !erro &&
        exerciciosFiltrados.length === 0 && (
          <div className="academia-empty">
            <div className="academia-empty__icon">
              <Dumbbell size={26} aria-hidden="true" />
            </div>

            <h2>
              {pesquisa
                ? "Nenhum exercício encontrado"
                : "Nenhum exercício cadastrado"}
            </h2>

            <p>
              {pesquisa
                ? "Tente pesquisar por outro nome ou grupo muscular."
                : "Cadastre seu primeiro exercício para começar."}
            </p>

            {!pesquisa && (
              <button
                type="button"
                onClick={abrirModal}
              >
                <Plus size={17} aria-hidden="true" />
                Cadastrar exercício
              </button>
            )}
          </div>
        )}

      {!carregando &&
        !erro &&
        exerciciosFiltrados.length > 0 && (
          <div className="exercise-grid">
            {exerciciosFiltrados.map((exercicio) => (
              <article
                className="exercise-card"
                key={exercicio.id}
              >
                <div className="exercise-card__icon">
                  <Dumbbell
                    size={21}
                    aria-hidden="true"
                  />
                </div>

                <div className="exercise-card__content">
                  <h2>{exercicio.nome}</h2>
                  <p>{exercicio.grupo_muscular}</p>
                </div>
              </article>
            ))}
          </div>
        )}

      {modalAberto && (
        <div
          className="exercise-modal-backdrop"
          role="presentation"
          onMouseDown={(evento) => {
            if (evento.target === evento.currentTarget) {
              fecharModal();
            }
          }}
        >
          <section
            className="exercise-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="exercise-modal-title"
          >
            <header className="exercise-modal__header">
              <div>
                <p>Novo cadastro</p>
                <h2 id="exercise-modal-title">
                  Novo exercício
                </h2>
              </div>

              <button
                type="button"
                onClick={fecharModal}
                disabled={salvando}
                aria-label="Fechar modal"
              >
                <X size={20} aria-hidden="true" />
              </button>
            </header>

            <form
              className="exercise-form"
              onSubmit={enviarFormulario}
            >
              <label className="exercise-field">
                <span>Nome</span>

                <input
                  autoFocus
                  required
                  type="text"
                  name="nome"
                  value={formulario.nome}
                  onChange={atualizarCampo}
                  placeholder="Ex.: Supino reto"
                  maxLength={100}
                />
              </label>

              {sugestoes.length > 0 && (
                <div className="exercise-suggestions">
                  <span>Exercícios parecidos</span>

                  <div className="exercise-suggestions__list">
                    {sugestoes.map((exercicio) => (
                      <button
                        key={exercicio.id}
                        type="button"
                        onClick={() =>
                          selecionarSugestao(exercicio)
                        }
                      >
                        <strong>{exercicio.nome}</strong>
                        <small>
                          {exercicio.grupo_muscular}
                        </small>
                      </button>
                    ))}
                  </div>

                  <p>
                    Você ainda pode criar “
                    <strong>{formulario.nome.trim()}</strong>
                    ” como um exercício diferente.
                  </p>
                </div>
              )}

              <label className="exercise-field">
                <span>Grupo muscular</span>

                <input
                  required
                  type="text"
                  name="grupo_muscular"
                  value={formulario.grupo_muscular}
                  onChange={atualizarCampo}
                  placeholder="Ex.: Peitoral"
                  maxLength={60}
                />
              </label>

              {erroFormulario && (
                <div
                  className="academia-message academia-message--error"
                  role="alert"
                >
                  {erroFormulario}
                </div>
              )}

              <footer className="exercise-form__actions">
                <button
                  className="exercise-button exercise-button--secondary"
                  type="button"
                  onClick={fecharModal}
                  disabled={salvando}
                >
                  Cancelar
                </button>

                <button
                  className="exercise-button exercise-button--primary"
                  type="submit"
                  disabled={salvando}
                >
                  <Plus size={17} aria-hidden="true" />

                  {salvando
                    ? "Criando..."
                    : formulario.nome.trim()
                      ? `Criar “${formulario.nome.trim()}”`
                      : "Criar exercício"}
                </button>
              </footer>
            </form>
          </section>
        </div>
      )}
    </section>
  );
}

export default AcademiaPage;
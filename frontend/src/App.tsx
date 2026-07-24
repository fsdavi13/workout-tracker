import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import AppLayout from "./layouts/AppLayout";
import AcademiaPage from "./pages/AcademiaPage";
import CorridasPage from "./pages/CorridasPage";
import DashboardPage from "./pages/DashboardPage";
import DietaPage from "./pages/DietaPage";
import NotFoundPage from "./pages/NotFoundPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route
            path="academia"
            element={<AcademiaPage />}
          />
          <Route
            path="corridas"
            element={<CorridasPage />}
          />
          <Route path="dieta" element={<DietaPage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
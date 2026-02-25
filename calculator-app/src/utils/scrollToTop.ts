import { useLocation } from "react-router-dom";
import { useEffect } from "react";


function ScrollToTop(): null {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0); // Прокрутка вверх при изменении пути
  }, [pathname]);

  return null;
}

export default ScrollToTop
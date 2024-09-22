import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'
import python_logo from '../../images/technologies/./Python-logo.png'
import js_logo from '../../images/technologies/./JavaScript-logo.png'
import dj_logo from '../../images/technologies/./django-logo2.png'
import docker_logo from '../../images/technologies/./docker-logo.png'
import drf_logo from '../../images/technologies/./DRF-logo.png'
import github_logo from '../../images/technologies/./github-logo.png'
import nginx_logo from '../../images/technologies/./nginx-logo.png'
import pg_logo from '../../images/technologies/./PG-logo.png'
import react_logo from '../../images/technologies/./react-logo.png'
import gunicorn_logo from '../../images/technologies/./gunicorn-logo.png'


const Technologies = () => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - Технологии" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Технологии</h1>
      <div className={styles.content}>
        <div>
          <div className={styles.logos}>
            <img src={js_logo} alt="Js Logo" />
            <img src={react_logo} alt="React Logo" />
            <img src={python_logo} alt="Python Logo" />
            <img src={dj_logo} alt="Django Logo" />
            <img src={drf_logo} alt="DRF Logo" />
            <img src={gunicorn_logo} alt="Gunicorn Logo" />
            <img src={pg_logo} alt="PgSQL Logo" />
            <img src={github_logo} alt="GitHub Logo" />
            <img src={nginx_logo} alt="Nginx Logo" />
            <img src={docker_logo} alt="Docker Logo" />
          </div>
        </div>
      </div>
      
    </Container>
  </Main>
}

export default Technologies


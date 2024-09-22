import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Привет!</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>А что это за сайт?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Представляю проект сайта продуктового помощника "Фудграм", созданный во время обучения в Яндекс Практикуме. Проект является финальной частью учебного курса, но создан полностью самостоятельно.
            </p>
            <p className={styles.textItem}>
              Продуктовый помощник позволяет создавать и хранить рецепты на онлайн-платформе. Можно скачать список продуктов, необходимых для
              приготовления блюда, посмотреть рецепты друзей, подписаться на интересных авторов и добавить любимые рецепты в список избранного.
            </p>
            <p className={styles.textItem}>
              Чтобы использовать все возможности сайта — нужна регистрация. Проверка адреса электронной почты не осуществляется, вы можете ввести любой email. 
            </p>
            <p className={styles.textItem}>
              Заходите и делитесь своими любимыми рецептами!
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Ссылки
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Исходный код проекта: <a href="https://github.com/Alexshifter/foodgram.git" className={styles.textLink}>Github</a>
            </p>
            <p className={styles.textItem}>
              Автор проекта: <a href="https://github.com/Alexshifter" className={styles.textLink}>Alexshifter</a>
            </p>
          </div>
        </aside>
      </div>
      
    </Container>
  </Main>
}

export default About

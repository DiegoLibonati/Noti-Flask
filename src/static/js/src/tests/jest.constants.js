export const BODY_ELEMENTS = `

    <body>

        <textarea
          id="note-content"
          class="c-note__text-area js-text-area"
          disabled
        ></textarea>

        <button
            type="button"
            aria-label="edit note"
            class="c-note__action c-note__action-confirm-edit o-button o-button-rounded-full o-button-fill-secondary js-btn-confirm-edit-note"
        >
            <i class="fa fa-check c-note__icon" aria-hidden="true"></i>
        </button>

        <button
            type="button"
            aria-label="add note"
            class="c-button-add o-button o-button-rounded-full o-button-fill-secondary js-btn-add-note"
        >
            <i class="fa fa-plus c-button-add__icon" aria-hidden="true"></i>
        </button>

        <button
            type="button"
            aria-label="edit note"
            class="c-note__action c-note__action-edit o-button o-button-rounded-full o-button-fill-secondary js-btn-edit-note"
        >
            <i class="fa fa-pencil c-note__icon" aria-hidden="true"></i>
        </button>

        <button
            type="button"
            aria-label="delete note"
            class="c-note__action c-note__action-delete o-button o-button-rounded-full o-button-fill-error js-btn-delete-note"
        >
            <i class="fa fa-trash c-note__icon" aria-hidden="true"></i>
        </button>

        <li
            class="c-alert c-alert--{{ category }} js-alert"
            id="js-alert-{{loop.index}}"
        >
            <div class="c-alert__wrapper-text">
                <h2 class="c-alert__text">{{ message }}</h2>
            </div>

            <button
                type="button"
                aria-label="btn close alert"
                class="c-alert__btn-close js-close-alert"
                id="js-close-alert-{{loop.index}}"
            >
                <img
                    src="{{ url_for('static', filename='assets/close-white.svg') }}"
                    alt="close alert"
                    class="c-alert__btn-close-image"
                />
            </button>
        </li>

        <nav class="c-nav js-navbar">
            <ul class="c-nav__list">
                <li class="c-nav__item" title="Home">
                    <a
                        href=""
                        target="_self"
                        class="c-nav__link {{ 'c-nav__link--active' if context['current_route'] == 'Home' }}"
                        aria-label="home"
                    >
                        <div class="c-nav__wrapper-icon">
                            <i class="fa fa-home c-nav__icon" aria-hidden="true"></i>
                        </div>
                        <h2 class="c-nav__text">Home</h2>
                    </a>
                </li>

                <li class="c-nav__item" title="Logout">
                    <a
                        target="_self"
                        class="c-nav__link c-nav__logout js-btn-logout"
                        aria-label="home"
                    >
                        <div class="c-nav__wrapper-icon">
                            <i class="fa fa-sign-out c-nav__icon" aria-hidden="true"></i>
                        </div>
                        <h2 class="c-nav__text">Logout</h2>
                    </a>
                </li>
            </ul>
        </nav>

        <div class="c-header__wrapper-actions">
          <button
            class="c-header__action c-header__action-open c-header__action--active js-open-navbar"
            aria-label="btn open navbar"
          >
            <i class="fa fa-bars c-header__action-icon" aria-hidden="true"></i>
          </button>
          <button
            class="c-header__action c-header__action-close js-close-navbar"
            aria-label="btn close navbar"
          >
            <i class="fa fa-close c-header__action-icon" aria-hidden="true"></i>
          </button>
        </div>

        <button
            class="c-form-auth__action-login o-button o-button-full o-button-rounded o-button-fill-primary js-btn-login"
            type="submit"
            aria-label="login"
        >
            LOGIN
        </button>

        <button
            class="c-form-auth__action-register o-button o-button-full o-button-rounded o-button-fill-primary js-btn-register"
            type="submit"
            aria-label="register"
        >
            REGISTER
        </button>

        <input
            class="c-form-auth__input js-input"
            type="text"
            id="username"
            name="username"
            placeholder="Username"
        />

        <input
            class="c-form-auth__input js-input"
            type="password"
            id="password"
            name="password"
            placeholder="Your password"
        />

        <input
            class="c-form-auth__input js-input"
            type="email"
            id="email"
            name="email"
            placeholder="user@gmail.com"
        />

    </body>

`;

export const BODY_LOGIN = `

    <main class="c-main-login o-main o-main-center o-main-secondary">
        <section
            class="c-container-wrapper-login o-container-center o-container-screen"
        >
            <form method="post" class="c-form-auth c-form-auth-login qa-form-login">
                <h2 class="c-form-auth__title">Member Login</h2>

                <input
                    class="c-form-auth__input js-input qa-input"
                    type="text"
                    id="username"
                    name="username"
                    placeholder="Username"
                />

                <input
                    class="c-form-auth__input js-input qa-input"
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Your password"
                />

                <button
                    class="c-form-auth__action-login o-button o-button-full o-button-rounded o-button-fill-primary js-btn-login"
                    type="submit"
                    aria-label="login"
                >
                    LOGIN
                </button>

                <a
                    class="c-form-auth__action-create-account o-button o-button-full o-button-rounded o-button-fill-primary"
                    href="{{ url_for(context['sign_up_view']) }}"
                    aria-label="create an account"
                    target="_self"
                >
                    Create an account
                </a>

                <div class="c-form-auth__wrapper-image">
                    <i class="fa fa-person c-form-auth__icon qa-form-icon" aria-hidden="true"></i>
                </div>
            </form>
        </section>
    </main>

`;

export const BODY_REGISTER = `

    <main class="c-main-register o-main o-main-center o-main-secondary">
        <section class="c-container-wrapper-register o-container-center o-container-screen">
            <form
                method="POST"
                class="c-form-auth c-form-auth-register qa-form-register"
            >
                <h2 class="c-form-auth__title">Member Register</h2>

                <input
                    class="c-form-auth__input js-input qa-input"
                    type="text"
                    id="username"
                    name="username"
                    placeholder="Username"
                />

                <input
                    class="c-form-auth__input js-input qa-input"
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Your password"
                />

                <input
                    class="c-form-auth__input js-input qa-input"
                    type="email"
                    id="email"
                    name="email"
                    placeholder="user@gmail.com"
                />

                <button
                    class="c-form-auth__action-register o-button o-button-full o-button-rounded o-button-fill-primary js-btn-register"
                    type="submit"
                    aria-label="register"
                >
                    REGISTER
                </button>

                <a
                    class="c-form-auth__action-have-account o-button o-button-full o-button-rounded o-button-fill-primary"
                    href="{{ url_for(context['login_view']) }}"
                    aria-label="do you already have an account?"
                    target="_self"
                >
                    Do you already have an account?
                </a>

                <div class="c-form-auth__wrapper-image">
                    <i class="fa fa-registered c-form-auth__icon qa-form-icon" aria-hidden="true"></i>
                </div>
            </form>
        </section>
    </main>

`;

export const BODY_HOME = `

    <main class="o-main o-main-app"></main>

`
# Love Fitness
![Original project responsive mockup](readme/amiresponsive/amiresponsive.PNG)

Love Fitness is a Django fitness storefront with product browsing, shopping and checkout, customer accounts, a Fitness Hub, and optional AI-powered product recommendations, workout building, and meal planning. A live demo is not currently available.

## Table of Contents
[Target audience](#target-audience) · [Project goals](#project-goals) · [Structure](#structure) · [Wireframes](#wireframes) · [Surface](#surface) · [Database](#database) · [Features](#features) · [Technologies](#technologies-used) · [Testing](#testing) · [Deployment](#deployment) · [Credits](#credits) · [Acknowledgements](#acknowledgements)

## Target Audience
Love Fitness is for people starting or maintaining a fitness routine, from beginners to experienced gym-goers. The store and guidance tools support customers looking for activewear, training equipment, nutrition products, and general fitness inspiration.

## Project Goals
The site aims to make fitness products and general training inspiration easy to discover, provide a straightforward purchase flow, and support a fitness community. Store management is restricted to authorized administrators.

## Structure
Love Fitness is a responsive fitness and activewear storefront built with Django and Bootstrap. Its pages are organized around browsing products, getting fitness guidance, and completing purchases. The main navigation is responsive and provides access to shopping, plans, the fitness hub, and account features.

The main areas of the site are:

1. **Home:** Introduces the store and links to product categories, fitness articles, and the AI product finder, workout builder, and nutrition planner.
2. **Account:** Visitors can register, sign in, and sign out. Signed-in customers can update delivery details and view their own order history.
3. **Shop:** Visitors can browse, search, filter, and sort activewear, fitness equipment, nutrition products, and plans. Product detail pages show product information and provide options such as adding an item to the bag or wishlist.
4. **Shopping bag:** Displays selected products, quantities, sizes, item subtotals, delivery costs, and the order total. Customers can update quantities, remove items, or continue to checkout.
5. **Checkout and order confirmation:** Customers enter delivery details and pay by card through Stripe. A successful order has a confirmation page and is included in the signed-in customer's order history.
6. **Wishlist:** Signed-in customers can save products for later and remove them from their wishlist.
7. **Fitness hub:** Visitors can read fitness articles and comments. Signed-in authors can create posts; authors and staff can edit or delete posts.
8. **AI Product Finder:** Visitors can get catalogue-based product suggestions using a description, optional category, and maximum budget.
9. **AI Workout Builder:** Visitors can request a general workout routine based on their goals, experience, schedule, equipment, location, and optional limitations.
10. **AI Nutrition Planner:** Visitors can request general meal ideas based on their preferences, food restrictions, schedule, cooking time, and budget. It does not provide calorie or macro targets.
11. **Contact:** Visitors can submit a message to the site owner.
12. **Store management:** Authorized store administrators can add, edit, and remove products.

The AI tools require an `OPENAI_API_KEY` configured on the server. Visitors must consent before their requests are sent to OpenAI. The product finder recommends only matching in-stock catalogue items; the workout and nutrition builders provide general suggestions, not medical advice.
---

## Skeleton
The refreshed wireframes below use a Balsamiq-inspired, low-fidelity style and reflect the current site, including the AI builders and account, shopping, and content-management flows. They are SVG illustrations, not native Balsamiq project files. The original Balsamiq PNG exports are preserved in `readme/wireframes/`.

## Wireframes
These desktop layouts are illustrative, not pixel-perfect specifications. Select a page to view its wireframe.

<details>
<summary>Home</summary>
<img src="readme/wireframes/wireframe_home.svg" alt="Home wireframe with hero, shop categories, AI builder links, and recent articles">
</details>

<details>
<summary>Product catalogue</summary>
<img src="readme/wireframes/wireframe_products.svg" alt="Product catalogue wireframe with category links, search, sorting, and product cards">
</details>

<details>
<summary>Product details</summary>
<img src="readme/wireframes/wireframe_product_details.svg" alt="Product details wireframe with image, price, options, add-to-bag, and wishlist actions">
</details>

<details>
<summary>Shopping bag</summary>
<img src="readme/wireframes/wireframe_bag.svg" alt="Shopping bag wireframe with product rows, quantity updates, remove buttons, and checkout">
</details>

<details>
<summary>Checkout</summary>
<img src="readme/wireframes/wireframe_checkout.svg" alt="Checkout wireframe with order summary, delivery form, Stripe card element, and order action">
</details>

<details>
<summary>Checkout success</summary>
<img src="readme/wireframes/wireframe_checkout_success.svg" alt="Order confirmation wireframe with reference, order summary, and delivery information">
</details>

<details>
<summary>Contact</summary>
<img src="readme/wireframes/wireframe_contact_us.svg" alt="Contact form wireframe with name, email, subject, message, and send action">
</details>

<details>
<summary>Fitness hub</summary>
<img src="readme/wireframes/wireframe_blog.svg" alt="Fitness hub wireframe with article summaries and post actions">
</details>

<details>
<summary>Blog article</summary>
<img src="readme/wireframes/wireframe_blog_detail.svg" alt="Blog article wireframe with post content and comments">
</details>

<details>
<summary>Create blog post</summary>
<img src="readme/wireframes/wireframe_blog_add_blog.svg" alt="Create blog post wireframe with title, subtitle, body, and publish action">
</details>

<details>
<summary>Edit blog post</summary>
<img src="readme/wireframes/wireframe_blog_edit.svg" alt="Edit blog post wireframe with editable title, subtitle, body, and save action">
</details>

<details>
<summary>Delete blog post</summary>
<img src="readme/wireframes/wireframe_blog_delete.svg" alt="Delete blog post confirmation wireframe with cancel and delete actions">
</details>

<details>
<summary>Account profile</summary>
<img src="readme/wireframes/wireframe_profile.svg" alt="Account profile wireframe with delivery details and order history">
</details>

<details>
<summary>Order details</summary>
<img src="readme/wireframes/wireframe_order_history.svg" alt="Order details wireframe with order reference, purchased items, totals, and delivery address">
</details>

<details>
<summary>Wishlist</summary>
<img src="readme/wireframes/wireframe_wishlist.svg" alt="Wishlist wireframe with saved product rows and remove actions">
</details>

<details>
<summary>Add product</summary>
<img src="readme/wireframes/wireframe_products_add_products.svg" alt="Add product wireframe with catalogue fields and add action">
</details>

<details>
<summary>Edit product</summary>
<img src="readme/wireframes/wireframe_products_edit_products.svg" alt="Edit product wireframe with catalogue fields, save, and delete actions">
</details>

<details>
<summary>Register</summary>
<img src="readme/wireframes/wireframe_register.svg" alt="Registration wireframe with account fields and create-account action">
</details>

<details>
<summary>Sign in</summary>
<img src="readme/wireframes/wireframe_sign_in.svg" alt="Sign-in wireframe with credentials, password recovery, and account link">
</details>

<details>
<summary>Sign out</summary>
<img src="readme/wireframes/wireframe_sign_out.svg" alt="Sign-out confirmation wireframe with cancel and sign-out actions">
</details>

<details>
<summary>AI Workout Builder</summary>
<img src="readme/wireframes/wireframe_ai_workout_builder.svg" alt="AI Workout Builder wireframe showing the privacy notice, workout preference form, consent, and generated routine area">
</details>

<details>
<summary>AI Nutrition Planner</summary>
<img src="readme/wireframes/wireframe_ai_nutrition_builder.svg" alt="AI Nutrition Planner wireframe showing the nutrition notice, meal preference form, allergy field, consent, and generated meal ideas area">
</details>

---

## Surface

Love Fitness uses a clean, responsive storefront design with generous spacing, clear page sections, and product photography. Dark headings and body text contrast with light backgrounds, while bright lime accents highlight key actions and links. Product cards, forms, and navigation use consistent borders, spacing, and button styles across desktop and mobile layouts.

## Colours
- **Charcoal / near-black** for strong headings, navigation text, and dark section backgrounds.
- **Lime green** for primary buttons, active states, and highlights.
- **Off-white and white** for page backgrounds, cards, and form surfaces.
- **Muted grey and green** for secondary text, borders, and supporting details.

## Typography
The Love Fitness logo uses its supplied SVG artwork. The site uses **Barlow Condensed** for prominent display headings and **DM Sans** for readable body text and form controls. Some home-page and navigation components also use **Exo**, **Exo 2**, and **Montserrat** for headings, labels, and supporting text. The layout scales typography and spacing for smaller screens.

## Database
Local development uses SQLite by default. PostgreSQL can be configured for deployment through the `DATABASE_URL` environment variable.

### Physical database model

The diagram shows the current application data models and their relationships. Django and django-allauth also create framework-managed tables for authentication, sessions, email addresses, and related account data; those tables are not expanded here.

![Current Love Fitness physical database model](readme/misc/physical_database_model.svg)

#### Application models

| Model | Main fields | Relationships |
|---|---|---|
| `User` (Django) | Username, password hash, names, email, staff/active/superuser flags, login and join timestamps | One-to-one with `UserProfile` and `Favourites`; one-to-many with blog posts |
| `UserProfile` | Default phone number, street addresses, town/city, county, postcode, country | One-to-one with `User`; one-to-many with orders |
| `Category` | Name, friendly name | One-to-many with products |
| `Product` | Name, description, gender, colour, size flag, price, stock quantity, rating, image URL, image | Optional many-to-one relationship with `Category`; referenced by order line items and favourites |
| `Order` | Order number, purchaser profile, customer and delivery details, date, delivery cost, item total, grand total, original bag, Stripe payment-intent ID | Optional many-to-one relationship with `UserProfile`; one-to-many with order line items |
| `OrderLineItem` | Product size, quantity, line-item total | Many-to-one relationships with `Order` and `Product` |
| `Favourites` (wishlist) | User, saved products | One-to-one relationship with `User`; many-to-many relationship with `Product` |
| `Post` | Title, title tag, author, body, post date | Many-to-one relationship with `User` |
| `Contact` | Full name, subject, email, message | No model relationships |

The AI Workout Builder and AI Nutrition Planner do not create database records for generated responses. Visitors must consent before their submitted answers are sent to OpenAI.

# Features
Love Fitness brings together an activewear and fitness-products store, account tools, fitness articles, and AI-assisted general guidance.
The screenshots below show the current site; account and order examples use fictional demo data.

### Navigation and responsive layout
- The responsive navigation provides links to the home page, product catalogue, exercise and nutrition plan categories, AI tools, Fitness Hub, and account options.
- On smaller screens, navigation is available through a collapsible menu. The site also includes links to the shopping bag, wishlist, and account pages.
> ![Desktop navigation](readme/features/features_nav_bar.PNG)
> ![Mobile navigation](readme/features/features_mobile_nav.PNG)

### Home page and fitness hub
- The home page highlights the store's product categories and links directly to the AI builders and Fitness Hub.
- Recent fitness articles are shown on the home page. The Fitness Hub provides the article listing and individual article pages.
- Signed-in users can create blog posts. Post authors and staff can edit or delete posts.
> ![Home page](readme/features/features_home.PNG)
> ![Fitness Hub](readme/features/features_fitness_hub.PNG)

### Product catalogue and details
- Visitors can browse products, filter by category, search the catalogue, and sort results.
- Product cards show key product information and link to a detail page. Product details include the description, price, stock and available purchase options.
- Signed-in customers can save products to a wishlist and remove them later.
- The AI Product Finder can suggest matching products using a shopper's request, optional category, and budget. It considers only in-stock products that match those filters, and displayed product names, prices, images, and links come from the catalogue.
- Visitors must consent before their request is sent to OpenAI. Requests are not saved to their Love Fitness account; browsing and shopping remain available without using AI.
> ![Product catalogue](readme/features/features_products.PNG)
> ![Shop category menu](readme/features/features_sort_products_via_nav.PNG)
> ![Search products](readme/features/features_search.PNG)
> ![Sort products](readme/features/features_sort_products_via_sort_by.PNG)
> ![Product details](readme/features/feature_product_details.PNG)
> ![Wishlist](readme/features/features_wishlist.PNG)

### Store management
- Staff can add, edit, and delete catalogue products through protected management pages.
> ![Add products](readme/features/features_add_products.PNG)
> ![Edit products](readme/features/features_edit_product.PNG)

### Accounts, profiles, and orders
- Visitors can register, sign in, and sign out. Signed-in customers can update their default delivery details and view their order history.
- Order history is restricted to the account that owns the orders. Guest checkout confirmation is limited to the browser session that placed the order.
> ![Sign in](readme/features/features_sign_in.PNG)
> ![Registration](readme/features/feature_register.PNG)
> ![Profile](readme/features/features_profile.PNG)
> ![Order history](readme/features/features_order_history.PNG)

### Shopping bag and checkout
- Customers can review the items in their bag, change quantities, remove items, or continue shopping.
- Checkout collects delivery details and processes card payments using Stripe. Customers see an order confirmation after a successful order, and an email confirmation is sent.
> ![Shopping bag](readme/features/features_bag.PNG)
> ![Checkout](readme/features/features_checkout.PNG)
> ![Checkout success](readme/features/features_checkout_success.PNG)

### Contact
- Visitors can use the contact form to send a message to the site owner.
> ![Contact form](readme/features/features_contact_us.PNG)

### AI Workout Builder
- Visitors can request a general workout routine based on their goal, experience, weekly availability, session length, equipment, location, and optional limitations.
- Visitors must consent before their answers are sent to OpenAI. Answers are not saved to their Love Fitness account.
- The page explains that the suggestions are not medical advice and recommends seeking professional guidance for injuries or health concerns.
- Workout results use structured output and are checked for the requested number of sessions before being displayed.
- Configure `OPENAI_API_KEY` on the server to enable generation. `OPENAI_MODEL` is optional and defaults to `gpt-4o-mini`.
> ![AI Workout Builder](readme/features/features_ai_workout_builder.PNG)

### AI Nutrition Planner
- Visitors can request general meal ideas based on their goal, dietary preferences, food allergies or restrictions, meals per day, cooking time, and budget.
- The planner does not provide calorie or macro targets, medical diets, or treatment advice. Visitors must consent before their answers are sent to OpenAI; answers are not saved to their Love Fitness account.
- Visitors are advised to check ingredients and food labels and to seek qualified professional advice for individualized nutrition needs.
- Meal-plan results use structured output and are checked for the requested number of meals before being displayed.
- The planner uses the same `OPENAI_API_KEY` and optional `OPENAI_MODEL` configuration as the AI Workout Builder.
> ![AI Nutrition Planner](readme/features/features_ai_nutrition_planner.PNG)

### AI Product Finder
- Visitors can describe what they are looking for and optionally narrow recommendations by catalogue category and maximum budget.
- The finder sends only matching in-stock catalogue records to OpenAI. It resolves returned recommendations against those records before displaying them, so AI output cannot supply product names, prices, availability, or links.
- Visitors must consent before their request is sent to OpenAI. Requests are not saved to their Love Fitness account. The regular catalogue and checkout do not depend on AI.
- The finder uses the same `OPENAI_API_KEY` and optional `OPENAI_MODEL` configuration as the other AI tools.

---

## Technologies Used
- **Python 3.10.18** and **Django 5.2.4** for the application backend.
- **HTML, CSS, and JavaScript** for page structure, styling, and browser interactions.
- **Bootstrap 5** and Django Crispy Forms for responsive layout and form rendering.
- **SQLite** for local development by default, with PostgreSQL supported through `DATABASE_URL`.
- **Stripe** for card-payment processing.
- **OpenAI API** for the optional product finder, workout builder, and nutrition planner.
- **Amazon S3** for optional static and media storage; WhiteNoise serves static assets when S3 is not enabled.

## Testing
Run the automated Django tests and framework checks from the repository root:

```bash
python manage.py test
python manage.py check
```

The suite completed successfully on 23 October 2026: 35 tests passed, and Django reported no system-check issues. Rerun the checks after making changes.

## Code Validation
The screenshots and third-party validation results below are historical project evidence from an earlier version of the interface; they are not a current validation of every page or asset. Rerun the relevant validators against the current deployment before relying on those results.
### CSS Validation
I have used the W3C CSS Validation Service - Jigsaw to check that my CSS is valid

|    Page     |               Result                |                       Screenshot                     |
| :---------: | :---------------------------------: | :---------------------------------------------------:|
| Base CSS    | CSS Validation passed with 0 Errors | [View Results](readme/css_validation/base.css.PNG)   |
| Blog CSS    | CSS Validation passed with 0 Errors | [View Results](readme/css_validation/blog.css.PNG)   |
| Profile CSS | CSS Validation passed with 0 Errors | [View Results](readme/css_validation/profile.css.PNG)|
---

### HTML Validation
I have used the W3C Markup Validation Service to check my HTML is valid

|   Page                    |  Result  |                      Screenshot                                                       |
|:-------------------------:|:---------|:-------------------------------------------------------------------------------------:|
|   Home                    | 0 errors | [View Results](readme/html_validation/html_validation_home.PNG)                       |
|   Products                | 0 errors | [View Results](readme/html_validation/html_validation_products.PNG)                   |
|   Product Details         | 0 errors | [View Results](readme/html_validation/html_validation_product_details.PNG)            |
|   Add Products            | 0 errors | [View Results](readme/html_validation/html_validation_add_products.PNG)               |
|   Edit Products           | 0 errors | [View Results](readme/html_validation/html_validation_edit_products.PNG)              |
|   Bag                     | 0 errors | [View Results](readme/html_validation/html_validation_bag.PNG)                        |
|   Blog                    | 0 errors | [View Results](readme/html_validation/html_validation_blog.PNG)                       |
|   Add Blog                | 0 errors | [View Results](readme/html_validation/html_validation_blog_add_blog.PNG)              |
|   Change Password         | 0 errors | [View Results](readme/html_validation/html_validation_change_password.PNG)            |
|   Confirm Change Password | 0 errors | [View Results](readme/html_validation/html_validation_confirmed_password_changed.PNG) |
|   Password Reset          | 0 errors | [View Results](readme/html_validation/html_validation_confirmed_password_changed.PNG) |
|   Checkout                | 0 errors | [View Results](readme/html_validation/html_validation_checkout.PNG)                   |
|   Contact                 | 0 errors | [View Results](readme/html_validation/html_validation_contact.PNG)                    |
|   Profile                 | 0 errors | [View Results](readme/html_validation/html_validation_profile.PNG)                    |
|   Register                | 0 errors | [View Results](readme/html_validation/html_validation_register_account.PNG)           |
|   Log In                  | 0 errors | [View Results](readme/html_validation/html_validation_login.PNG)                      |
|   Log Out                 | 0 errors | [View Results](readme/html_validation/html_validation_logout.PNG)                     |
|   Wishlist                | 0 errors | [View Results](readme/html_validation/html_validation_wishlist.PNG)                   |
|   Verification Emai Sent  | 0 errors | [View Results](readme/html_validation/html_verification_email_sent.PNG)               |
---

### Javascript Validation
I have used JS Hint to validate my Javascript.

|     Page        |        Result           |                            Screenshot                 |
|:---------------:|:-----------------------:|:-----------------------------------------------------:|
| bag.js          |   0 errors, 0 warnings  | [View Results](readme/jshint/jshint_bag.PNG)          |
| carousel.js     |   0 errors, 0 warnings  | [View Results](readme/jshint/jshint_carousel.PNG)     |
| countryfield.js |   0 errors, 0 warnings  | [View Results](readme/jshint/jshint_countryfield.PNG) |
| stripe.js       |   0 errors, 0 warnings  | [View Results](readme/jshint/jshint_stripe.PNG)       |
| toast.js        |   0 errors, 0 warnings  | [View Results](readme/jshint/toast.PNG)               |

---

### Python
Each file was individually checked in (https://pep8online.com/) and any errors resolved. The entire project was then checked in PyCharm to produce a report.

|     Page                      |   Result             |
|:-----------------------------:|:--------------------:|
|   bag/admin.py                | No errors or warnings |
|   bag/apps.py                 | No errors or warnings |
|   bag/contexts.py             | No errors or warnings |
|   bag/models.py               | No errors or warnings |
|   bag/urls.py                 | No errors or warnings |
|   bag/views.py                | No errors or warnings |
|   contact/admin.py            | No errors or warnings |
|   contact/apps.py             | No errors or warnings |
|   contact/forms.py            | No errors or warnings |
|   contact/models.py           | No errors or warnings |
|   contact/urls.py             | No errors or warnings |
|   contact/views.py            | No errors or warnings |
|   checkout/admin.py           | No errors or warnings |
|   checkout/apps.py            | No errors or warnings |
|   checkout/forms.py           | No errors or warnings |
|   checkout/models.py          | No errors or warnings |
|   checkout/signals.py         | No errors or warnings |
|   checkout/urls.py            | No errors or warnings |
|   checkout/views.py           | No errors or warnings |
|   checkout/webhook_handler.py | No errors or warnings |
|   checkout/webhooks.py        | No errors or warnings |
|   wishlist/admin.py           | No errors or warnings |
|   wishlist/apps.py            | No errors or warnings |
|   wishlist/models.py          | No errors or warnings |
|   wishlist/urls.py            | No errors or warnings |
|   wishlist/views.py           | No errors or warnings |
|   home/admin.py               | No errors or warnings |
|   home/apps.py                | No errors or warnings |
|   home/forms.py               | No errors or warnings |
|   home/models.py              | No errors or warnings |
|   home/urls.py                | No errors or warnings |
|   home/views.py               | No errors or warnings |
|   products/admin.py           | No errors or warnings |
|   products/apps.py            | No errors or warnings |
|   products/forms.py           | No errors or warnings |
|   products/models.py          | No errors or warnings |
|   products/urls.py            | No errors or warnings |
|   products/views.py           | No errors or warnings |
|   products/widgets.py         | No errors or warnings |
|   profiles/admin.py           | No errors or warnings |
|   profiles/apps.py            | No errors or warnings |
|   profiles/forms.py           | No errors or warnings |
|   profiles/models.py          | No errors or warnings |
|   profiles/urls.py            | No errors or warnings |
|   profiles/views.py           | No errors or warnings |
|   products/widgets.py         | No errors or warnings |

After checking the Python files seperately and correctng any errors, I then used PyCharm to check all files within the project to provive a report.
[View Results](readme/testing/pep8/pep8.PNG)

### WAVE Accessibility

I have used the WAVE Web Accessibilty Evaluation Tool to ensure site is accessible

|   Page                    |  Result  |                      Screenshot                                                                          |
|:-------------------------:|:---------|:--------------------------------------------------------------------------------------------------------:|
|   Home                    | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_home.PNG)                       |
|   Products                | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_products.PNG)                   |
|   Product Details         | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_product_details.PNG)            |
|   Add Products            | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_add_products.PNG)               |
|   Edit Products           | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_edit_products.PNG)              |
|   Bag                     | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_bag.PNG)                        |
|   Blog                    | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_blog.PNG)                      |
|   Add Blog                | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_blog_add_blog.PNG)              |
|   Change Password         | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_change_password.PNG)            |
|   Confirm Change Password | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_change_password_confirmed.PNG)  |
|   Password Reset          | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_password_reset.PNG)             |
|   Checkout                | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_checkout.PNG)                   |
|   Checkout Success        | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_checkout_success.PNG)           |
|   Contact                 | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_contact.PNG)                    |
|   Profile                 | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_profile.PNG)                    |
|   Register                | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_register.PNG)                   |
|   Log In                  | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_login.PNG)                      |
|   Log Out                 | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_logout.PNG)                     |
|   Wishlist                | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_view_wishlist.PNG)              |
|   Verification Emai Sent  | 0 errors, 0 contrast errors | [View Results](readme/wave_validation/wave_validation_verification_email_sent.PNG)    |
--- 

### Lighthouse Performance
I have used Google Lighthouse (in Google Dev tools) to measure the performance the site

|   Page                              |  Result                                                         |                      Screenshot                                    |
|:-----------------------------------:|:----------------------------------------------------------------|:------------------------------------------------------------------:|
|   Home - Desktop                    | 92 Performance, 91 Accessibility, 100 Best Practices, 89 SEO    | [View Results](readme/lighthouse/desktop/home.PNG)                 |
|   Products - Desktop                | 98 Performance, 92 Accessibility, 100 Best Practices, 90 SEO    | [View Results](readme/lighthouse/desktop/products.PNG)             |
|   Product Details - Desktop         | 99 Performance, 92 Accessibility, 100 Best Practices, 90 SEO    | [View Results](readme/lighthouse/desktop/product_details.PNG)      |
|   Add Products - Desktop            | 100 Performance, 81 Accessibility, 100 Best Practices, 78 SEO   | [View Results](readme/lighthouse/desktop/add_product.PNG)          |
|   Edit Products - Desktop           | 100 Performance, 85 Accessibility, 100 Best Practices, 80 SEO   | [View Results](readme/lighthouse/desktop/edit_product.PNG)         |
|   Bag - Desktop                     | 98 Performance, 81 Accessibility, 100 Best Practices, 80 SEO    | [View Results](readme/lighthouse/desktop/bag.PNG)                  |
|   Blog - Desktop                    | 100 Performance, 87 Accessibility, 100 Best Practices, 78 SEO   | [View Results](readme/lighthouse/desktop/blog.PNG)                 |
|   Add Blog - Desktop                | 99 Performance, 91 Accessibilty, 100 Best Practices, 78 SEO     | [View Results](readme/lighthouse/desktop/add_blog.PNG)             |
|   Change Password - Desktop         | 99 Performance, 91 Accessibilty, 100 Best Practices, 89 SEO     | [View Results](readme/lighthouse/desktop/password_reset.PNG)       |
|   Confirm Change Password - Desktop | 99 Performance, 91 Accessibilty, 100 Best Practices, 89 SEO     | [View Results](readme/lighthouse/desktop/change_password_conf.PNG) |
|   Checkout - Desktop                | 99 Performance, 93 Accessibilty, 100 Best Practices, 80 SEO     | [View Results](readme/lighthouse/desktop/checkout.PNG)             |
|   Checkout Success - Desktop        | 98 Performance, 90 Accessibilty, 100 Best Practices, 78 SEO     | [View Results](readme/lighthouse/desktop/checkout_success.PNG)     |
|   Contact - Desktop                 | 99 Performance, 90 Accessibilty, 100 Best Practices, 89 SEO     | [View Results](readme/lighthouse/desktop/contact.PNG)              |
|   Profile - Desktop                 | 99 Performance, 90 Accessibilty, 100 Best Practices, 89 SEO     | [View Results](readme/lighthouse/desktop/profile.PNG)              |
|   Register - Desktop                | 99 Performance, 91 Accessibilty, 100 Best Practices, 89 SEO     | [View Results](readme/lighthouse/desktop/sign_up.PNG)              |
|   Log In - Desktop                  | 99 Performance, 91 Accessibilty, 100 Best Practices, 89 SEO     | [View Results](readme/lighthouse/desktop/sign_in.PNG)              |
|   Log Out - Desktop                 | 99 Performance, 91 Accessibilty, 100 Best Practices, 78 SEO     | [View Results](readme/lighthouse/desktop/sign_out.PNG)             |
|   Wishlist - Desktop                | 100 Performance, 90 Accessibilty, 100 Best Practices, 80 SEO    | [View Results](readme/lighthouse/desktop/wish_list.PNG)            |
|   Order History - Desktop           | 99 Performance, 93 Accessibilty, 100 Best Practices, 78 SEO     | [View Results](readme/lighthouse/desktop/order_history.PNG)        |
>
|   Page                             |  Result                                                      |                      Screenshot                                   |
|:----------------------------------:|:-------------------------------------------------------------|:-----------------------------------------------------------------:|
|   Home - Mobile                    | 69 Performance, 91 Accessibility, 100 Best Practices, 91 SEO | [View Results](readme/lighthouse/mobile/home.PNG)                 |
|   Products - Mobile                | 64 Performance, 90 Accessibility, 93 Best Practices, 91 SEO  | [View Results](readme/lighthouse/mobile/products.PNG)             |
|   Product Details - Mobile         | 84 Performance, 90 Accessibility, 100 Best Practices, 82 SEO | [View Results](readme/lighthouse/mobile/product_details.PNG)      |
|   Add Products - Mobile            | 92 Performance, 81 Accessibility, 100 Best Practices, 80 SEO | [View Results](readme/lighthouse/mobile/add_product.PNG)          |
|   Edit Products - Mobile           | 91 Performance, 82 Accessibility, 100 Best Practices, 82 SEO | [View Results](readme/lighthouse/mobile/edit_product.PNG)         |
|   Bag - Mobile                     | 91 Performance, 88 Accessibility, 100 Best Practices, 79 SEO | [View Results](readme/lighthouse/mobile/bag.PNG)                  |
|   Blog - Mobile                    | 91 Performance, 84 Accessibility, 100 Best Practices, 82 SEO | [View Results](readme/lighthouse/mobile/blog.PNG)                 |
|   Add Blog - Mobile                | 90 Performance, 88 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/add_blog.PNG)             |
|   Change Password - Mobile         | 99 Performance, 91 Accessibilty, 100 Best Practices, 78 SEO  | [View Results](readme/lighthouse/mobile/password_reset.PNG)       |
|   Confirm Change Password - Mobile | 90 Performance, 91 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/change_password_conf.PNG) |
|   Checkout - Mobile                | 91 Performance, 91 Accessibilty, 100 Best Practices, 81 SEO  | [View Results](readme/lighthouse/mobile/checkout.PNG)             |
|   Checkout Success - Mobile        | 91 Performance, 88 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/checkout_success.PNG)     |
|   Contact - Mobile                 | 92 Performance, 87 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/contact.PNG)              |
|   Profile - Mobile                 | 90 Performance, 89 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/profile.PNG)              |
|   Register - Mobile                | 91 Performance, 88 Accessibilty, 100 Best Practices, 89 SEO  | [View Results](readme/lighthouse/mobile/sign_up.PNG)              |
|   Log In - Mobile                  | 91 Performance, 88 Accessibilty, 100 Best Practices, 89 SEO  | [View Results](readme/lighthouse/mobile/sign_in.PNG)              |
|   Log Out - Mobile                 | 90 Performance, 88 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/sign_out.PNG)             |
|   Wishlist - Mobile                | 90 Performance, 88 Accessibilty, 93 Best Practices, 81 SEO   | [View Results](readme/lighthouse/mobile/wish_list.PNG)            |
|   Order History - Mobile           | 91 Performance, 90 Accessibilty, 100 Best Practices, 80 SEO  | [View Results](readme/lighthouse/mobile/order_history.PNG)        |
--- 

### Device Tests
Previous manual device-test notes and screenshots describe an earlier version of the site. They have not been re-run against the current interface and should not be treated as current compatibility results.

### Browser Tests
The repository does not include current cross-browser test results. Re-test the current site in supported browsers before release.

### User story tests
The automated Django suite covers core application behavior, including account and order access, blog permissions, checkout validation, and shopping-bag operations. Run `python manage.py test` for the current results. Older user-story screenshots are retained in `readme/testing/` as project history, not as verification of the current UI.

---

# Deployment

## Local setup

1. Clone the repository and enter the project directory:

   ```bash
   git clone https://github.com/JohnWrafter/Love_Fitness.git
   cd Love_Fitness
   ```

2. Use Python 3.10.18 (the version recorded in `.python-version`) and create and activate a virtual environment.
3. Install dependencies and apply database migrations:

   ```bash
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

4. Optionally create an administrator account:

   ```bash
   python manage.py createsuperuser
   ```

   Add catalogue products and categories through Django admin. The old product and plan fixtures mentioned in earlier versions of this README are not included in the repository.

5. Start the development server and visit `http://127.0.0.1:8000/`:

   ```bash
   python manage.py runserver
   ```

Local development uses SQLite by default and `DEBUG` defaults to true when `DATABASE_URL` is absent. Use environment variables or an ignored local `.env` file for local configuration; never put secrets in tracked files.

## Production deployment

The repository includes a Gunicorn `Procfile`. Configure the following environment variables in the hosting platform as appropriate:

- `SECRET_KEY`: private, unique value required when `DEBUG=False`.
- `DEBUG=False`.
- `DATABASE_URL`: production database connection URL; without it, Django uses SQLite.
- `ALLOWED_HOSTS`: comma-separated hostnames without URL schemes.
- `CSRF_TRUSTED_ORIGINS`: comma-separated trusted origins including `https://`.
- `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, and `STRIPE_WH_SECRET` for payments.
- `OPENAI_API_KEY` to enable the AI tools; `OPENAI_MODEL` is optional and defaults to `gpt-4o-mini`.
- For SMTP email, configure `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL`. Set `DEVELOPMENT` truthy to use the console email backend in development.

When `DEBUG=False`, HTTPS redirection, secure session and CSRF cookies, and one-year HSTS are enabled. Configure HTTPS and valid host/origin settings before launch. Run these commands during deployment after configuring the database and static storage:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Stripe

Configure Stripe API keys in the environment: `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, and `STRIPE_WH_SECRET`. Set a webhook endpoint at `/checkout/wh/` and subscribe it to `payment_intent.payment_failed` and `payment_intent.succeeded`. Use test-mode keys for local testing and never commit key values.

## Optional Amazon S3 storage

S3 storage is enabled when `USE_AWS` is present in the environment. The configured bucket is `lovefitness` in the `eu-west-2` region; configure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` using a secret manager. Grant the IAM identity only the bucket permissions the application requires. Do not enable broad public access or grant full-account permissions. Leave `USE_AWS` unset to use local media storage and WhiteNoise for static files.

## OpenAI

Set `OPENAI_API_KEY` to enable the AI tools. `OPENAI_MODEL` can optionally select another model available to the account and supported by the OpenAI Responses API; the default is `gpt-4o-mini`. Do not commit API keys.

---

### Credits

## Images
- Product photography is credited to Myprotein and Argos in the original project assets.
- The home-page hero image is sourced from Unsplash.

# Acknowledgements
> * Mo Shami for his internal patience and guidance
> * My partner who has not seen that much of me during MS4

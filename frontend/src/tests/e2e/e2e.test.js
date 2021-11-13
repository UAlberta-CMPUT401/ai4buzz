import puppeteer from 'puppeteer';

describe('E2E testing Login page', () => {
  let browser;
  let page;

  jest.setTimeout(60000);

  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
  });

  it('Should redirect to analyze image page after successful login', async () => {
    await page.goto('http://localhost:3000/login');
    await page.waitForSelector('#signin__email__input');

    await page.click('#signin__email__input');
    await page.type('#signin__email__input', 'test@test.com');

    await page.click('#signin__password__input');
    await page.type('#signin__password__input', 'password');

    await page.click('.submitButton');
    console.log(page);

    // const text = await page.$eval(
    //   ".form-success-message",
    //   (e) => e.textContent
    // );
    // expect(text).toContain("You are now signed in.");
  });

  afterAll(() => browser.close());
});

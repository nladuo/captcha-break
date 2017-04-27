from gen_captcha import load_templates, create_captcha
import os
import uuid

if __name__ == "__main__":
    templates = load_templates()

    for i in range(1000000):
        captcha, captcha_str = create_captcha(templates)
        save_path = os.path.join(".", "dataset", "%s-%s.png" % (captcha_str, str(uuid.uuid4())))
        with open(save_path, "wb") as f:
            captcha.save(f)
        print save_path

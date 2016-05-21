package main

import (
	"crypto/md5"
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"io"
	"net/http"
	"os"
)

func getMd5String(s string) string {
	h := md5.New()
	h.Write([]byte(s))
	return hex.EncodeToString(h.Sum(nil))

}

func getGuid() string {
	b := make([]byte, 48)

	if _, err := io.ReadFull(rand.Reader, b); err != nil {
		return ""
	}
	return getMd5String(base64.URLEncoding.EncodeToString(b))
}

func main() {
	for i := 0; i < 1000; i++ {

		doc, err := goquery.NewDocument("http://login.weibo.cn/login/")
		if err != nil {
			continue
		}
		doc.Find("img").Each(func(i int, contentSelection *goquery.Selection) {
			if i == 0 {
				imageURL, exist := contentSelection.Attr("src")
				if exist {
					fmt.Println(imageURL)
					resp, err := http.Get(imageURL)
					if err != nil {
						return
					}
					fmt.Println(resp.ContentLength)
					if resp.ContentLength != -1 {
						return
					}

					filename := "./captchas/" + getGuid() + ".gif"
					file, err := os.Create(filename)
					if err != nil {
						return
					}
					io.Copy(file, resp.Body)
					resp.Body.Close()
					fmt.Println(filename)
				}

			}
		})
	}

}

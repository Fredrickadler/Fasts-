import "./globals.css";

export const metadata = {
  title: "Flwy Frame",
  description: "A Farcaster Frame App",
  icons: {
    icon: "/icon.png",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <meta
          name="fc:frame"
          content='{
            "version":"next",
            "imageUrl":"https://flwy-one.vercel.app/preview.png",
            "button":{
              "title":"Open Flwy",
              "action":{
                "type":"launch_frame",
                "name":"Flwy",
                "url":"https://flwy-one.vercel.app",
                "splashImageUrl":"https://flwy-one.vercel.app/splash.png",
                "splashBackgroundColor":"#000000"
              }
            }
          }'
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
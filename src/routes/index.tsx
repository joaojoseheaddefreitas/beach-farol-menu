import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Beach Farol Itapuã — Cardápio e Comanda Digital" },
      {
        name: "description",
        content:
          "Cardápio digital, comanda e gestão do Beach Farol Itapuã: petiscos, moquecas, pratos especiais e bebidas em Salvador - BA.",
      },
      { property: "og:title", content: "Beach Farol Itapuã — Cardápio Digital" },
      {
        property: "og:description",
        content:
          "Peça pelo cardápio digital do Beach Farol Itapuã: petiscos, moquecas, pratos e bebidas geladas na praia de Itapuã.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <main className="h-[100dvh] w-full">
      <h1 className="sr-only">Beach Farol Itapuã — Cardápio Digital</h1>
      <iframe
        src="/app/index.html"
        title="Beach Farol Itapuã — Cardápio e Gestão"
        className="h-full w-full border-0"
      />
    </main>
  );
}

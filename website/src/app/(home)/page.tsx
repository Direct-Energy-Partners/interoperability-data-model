import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex flex-col justify-center text-center flex-1 gap-4 py-16">
      <h1 className="text-3xl font-bold">Interoperability Data Model</h1>
      <p className="text-fd-muted-foreground max-w-xl mx-auto">
        A common, machine readable model for microgrid electrical components,
        generated from the dcide-app validators. Browse the component guides and
        the auto generated schema reference.
      </p>
      <div>
        <Link
          href="/docs"
          className="inline-block font-medium rounded-md bg-fd-primary text-fd-primary-foreground px-4 py-2"
        >
          Open the documentation
        </Link>
      </div>
    </main>
  );
}

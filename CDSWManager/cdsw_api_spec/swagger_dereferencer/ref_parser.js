import $RefParser from "@apidevtools/json-schema-ref-parser";
import data from '../full_swagger.json' assert { type: 'json' };
import fs from 'fs';

try {
    console.log(data);
    await $RefParser.dereference(data);
    console.log(data);

    fs.writeFileSync('./test.json', JSON.stringify(data));

} catch (err) {
    console.error(err);
}